import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_input import read_transcript

def test_read_transcript():
    # Path to the test transcript file
    test_file_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')
    
    # Test reading the file
    content = read_transcript(test_file_path)
    assert content is not None, "Failed to read the test transcript file"
    assert "XYZ Corp" in content, "The test transcript content is not as expected"
    
    # Test reading a non-existent file
    content = read_transcript("non_existent_file.txt")
    assert content is None, "Reading a non-existent file should return None"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_read_transcript()