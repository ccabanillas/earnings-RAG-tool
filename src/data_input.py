import os
from .transcript_processing import embed_and_store_transcript

def read_transcript(file_path):
    """
    Read a transcript file and return its content as a string.
    
    Args:
    file_path (str): Path to the transcript file
    
    Returns:
    str: Content of the transcript file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except IOError:
        print(f"Error: Unable to read file at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None

def process_transcripts(directory):
    """
    Process all transcript files in the given directory.
    
    Args:
    directory (str): Path to the directory containing transcript files
    """
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            transcript = read_transcript(file_path)
            if transcript:
                transcript_id = os.path.splitext(filename)[0]
                embed_and_store_transcript(transcript_id, transcript)
                print(f"Processed and stored: {filename}")