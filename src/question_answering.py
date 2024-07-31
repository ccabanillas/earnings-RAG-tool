from .transcript_processing import process_and_answer

def answer_earnings_call_question(question, transcript_id=None):
    """
    Answer a question about earnings call transcripts.
    
    Args:
    question (str): The question to answer
    transcript_id (str, optional): Specific transcript ID to query, if any
    
    Returns:
    str: The answer to the question
    """
    return process_and_answer(question, transcript_id)