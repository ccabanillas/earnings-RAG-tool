import os
import openai
import pinecone
import tiktoken
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI and Pinecone
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))

# Choose the embedding model
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = "cl100k_base"

def get_encoding():
    return tiktoken.get_encoding(EMBEDDING_ENCODING)

def get_embedding(text):
    return openai.Embedding.create(input=[text], model=EMBEDDING_MODEL)["data"][0]["embedding"]

def chunk_transcript(transcript, max_tokens=500):
    encoding = get_encoding()
    tokens = encoding.encode(transcript)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i + max_tokens]
        chunks.append(encoding.decode(chunk))
    
    return chunks

def embed_and_store_transcript(transcript_id, transcript):
    index_name = "earnings-call-transcripts"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=1536)  # Dimension for text-embedding-ada-002
    
    index = pinecone.Index(index_name)
    chunks = chunk_transcript(transcript)
    
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        index.upsert([(f"{transcript_id}-{i}", embedding, {"text": chunk})])

def query_transcripts(query, top_k=5):
    index = pinecone.Index("earnings-call-transcripts")
    query_embedding = get_embedding(query)
    results = index.query(query_embedding, top_k=top_k, include_metadata=True)
    return [result.metadata["text"] for result in results.matches]

def answer_question(question, context):
    prompt = f"""
    You are an AI assistant specialized in analyzing earnings call transcripts.
    Use the following context from earnings call transcripts to answer the question.
    If the answer cannot be found in the context, say "I don't have enough information to answer that question."

    Context:
    {context}

    Question: {question}

    Answer:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes earnings call transcripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content

def process_and_answer(question, transcript_id=None):
    if transcript_id:
        context = query_transcripts(question, top_k=3)
    else:
        context = query_transcripts(question, top_k=5)
    
    context_text = "\n".join(context)
    return answer_question(question, context_text)