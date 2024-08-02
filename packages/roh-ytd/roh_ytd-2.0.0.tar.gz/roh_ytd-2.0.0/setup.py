from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="roh-ytd",
    version="2.0.0",  # Increment this version number
    description="A Python package for downloading YouTube videos and audio in various formats with a graphical user interface.",
    long_description=README,
    long_description_content_type='text/markdown',
    author="Rohan Kumar Bhoi",
    author_email="me.rohanbhoi@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "yt-dlp",
        "ttkthemes"
    ],
    entry_points={
        'console_scripts': [
            'roh-ytd=roh_ytd.downloader:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
