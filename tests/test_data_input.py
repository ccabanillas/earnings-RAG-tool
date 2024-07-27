import os
import sys
import io
from contextlib import redirect_stdout

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_input import read_transcript

def test_read_transcript():
    # Path to the test transcript file
    test_file_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')
    
    print("Test 1: Reading an existing file")
    content = read_transcript(test_file_path)
    assert content is not None, "Failed to read the test transcript file"
    assert "XYZ Corp" in content, "The test transcript content is not as expected"
    print("Test 1 passed: Successfully read the test transcript file")
    
    print("\nTest 2: Reading a non-existent file")
    # Capture the printed output
    f = io.StringIO()
    with redirect_stdout(f):
        content = read_transcript("non_existent_file.txt")
    output = f.getvalue()
    
    assert content is None, "Reading a non-existent file should return None"
    assert "Error: File not found" in output, "Expected error message not printed"
    print("Test 2 passed: Correctly handled non-existent file")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_read_transcript()