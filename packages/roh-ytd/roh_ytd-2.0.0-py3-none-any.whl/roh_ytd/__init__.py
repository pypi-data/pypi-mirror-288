"""
roh_ytd: A YouTube Downloader package
"""

__version__ = "0.1.0"
__author__ = "Rohan Kumar Bhoi"
__license__ = "MIT"

from .downloader import YouTubeDownloaderApp

# Optional: You can define some package-wide variables or functions here

def main():
    """Main function to run the YouTube Downloader app."""
    app = YouTubeDownloaderApp()
    app.run()
