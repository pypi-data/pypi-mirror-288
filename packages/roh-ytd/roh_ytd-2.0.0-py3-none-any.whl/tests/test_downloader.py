# tests/test_downloader.py

import pytest
import os
import tempfile
from roh_ytd.downloader import download_video, download_audio, open_folder

@pytest.fixture
def temp_dir():
    """Fixture to create and clean up a temporary directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

def test_download_video(temp_dir):
    """Test the download_video function."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with a valid URL or mock
    output_path = temp_dir
    
    # Since the actual download involves network and external dependencies,
    # you might want to use a mock or a test video URL.
    # For this example, it's assumed the URL is valid and downloadable.
    try:
        download_video(url, output_path)
        files = os.listdir(output_path)
        assert any(file.endswith(('.mp4', '.mkv', '.avi')) for file in files), "No video file downloaded"
    except Exception as e:
        pytest.fail(f"Download failed: {e}")

def test_download_audio(temp_dir):
    """Test the download_audio function."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with a valid URL or mock
    output_path = temp_dir

    # Since the actual download involves network and external dependencies,
    # you might want to use a mock or a test video URL.
    # For this example, it's assumed the URL is valid and downloadable.
    try:
        download_audio(url, output_path)
        files = os.listdir(output_path)
        assert any(file.endswith('.mp3') for file in files), "No audio file downloaded"
    except Exception as e:
        pytest.fail(f"Download failed: {e}")

def test_open_folder(temp_dir):
    """Test the open_folder function."""
    # Create a test file in the temporary directory
    test_file_path = os.path.join(temp_dir, "test_file.txt")
    with open(test_file_path, 'w') as f:
        f.write("This is a test file.")

    try:
        open_folder(test_file_path)
        # The function `open_folder` will attempt to open the directory
        # You may want to verify the behavior manually or use a mock
    except Exception as e:
        pytest.fail(f"Failed to open folder: {e}")

if __name__ == "__main__":
    pytest.main()
