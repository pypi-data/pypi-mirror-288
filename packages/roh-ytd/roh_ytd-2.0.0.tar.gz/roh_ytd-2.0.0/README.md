# roh-ytd

A Python package for downloading YouTube videos and audio in various formats. The package provides a graphical user interface (GUI) for an easy and interactive way to download videos or audio files from YouTube.

## Features

- Download YouTube videos in multiple formats (e.g., MP4, MKV).
- Download YouTube audio as MP3 files.
- Simple and user-friendly graphical interface.
- Progress tracking and error handling during download.
- Option to open the download folder directly from the application.

## System Requirements

- Python 3.6 or higher
- Internet connection for downloading content
- FFmpeg (for audio extraction)

## Installation

To install the roh-ytd package, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/Rohan-0707/roh-ytd.git
    ```
2. Navigate to the project directory:
    ```sh
    cd roh-ytd
    ```
3. Install the package using pip:
    ```sh
    pip install .
    ```

## Usage

1. **Run the application**:
    ```sh
    python -m roh_ytd.downloader
    ```
2. **Enter the URL of the YouTube video** you want to download.
3. **Select the output path** where the downloaded files will be saved.
4. **Choose the format** (Video or Audio).
5. Click **Download** to start the process.
6. Monitor the progress in the download dialog.

## Troubleshooting

- **Issue**: Application not starting.
  - **Solution**: Ensure you have Python 3.6+ installed and try reinstalling the package.

- **Issue**: Download errors or failures.
  - **Solution**: Check your internet connection and ensure the URL is correct. Also, make sure FFmpeg is installed and properly configured.

## FAQ

- **Q**: Can I download videos from private channels or videos?
  - **A**: No, the application only supports public YouTube videos.

- **Q**: What formats are supported for video and audio?
  - **A**: Supported video formats include MP4, MKV, AVI, and audio is downloaded as MP3.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [YouTube-DL](https://github.com/yt-dlp/yt-dlp) for the video and audio downloading functionality.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the graphical user interface components.
- [FFmpeg](https://ffmpeg.org/) for audio extraction.

## Developer Information

- **Name**: Rohan Kumar Bhoi
- **Email**: [me.rohanbhoi@gmail.com](mailto:me.rohanbhoi@gmail.com)
- **Social Media**:
  - Instagram: [ceorohan](https://instagram.com/ceorohan)
  - LinkedIn: [ceorohan](https://linkedin.com/in/ceorohan)
  - Twitter: [ceorohan1](https://twitter.com/ceorohan1)
