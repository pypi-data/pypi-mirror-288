from setuptools import setup, find_packages

setup(
    name="roh-ytd",
    version="1.0.0",  # Update to match your package version
    description="A Python package for downloading YouTube videos and audio in various formats with a graphical user interface.",
    author="Rohan Kumar Bhoi",
    author_email="me.rohanbhoi@gmail.com",
    license="MIT",  # Update to your license type
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
