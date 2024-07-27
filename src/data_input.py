import os

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