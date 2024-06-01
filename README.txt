SCH✿LΛR SCRΛPƎR

Welcome to the SCH✿LΛR SCRΛPƎR GitHub Wiki! This tool automates the process of downloading academic papers from Google Scholar.

Table of Contents

    Overview
    Features
    Installation
    Usage
    Configuration
    Troubleshooting
    Contributing
    Disclaimer

Overview

SCH✿LΛR SCRΛPƎR is a tool designed to help researchers and students download academic papers from Google Scholar. It automates the search and download process, providing a user-friendly interface to specify search queries and save locations.

Features

    Download academic papers from Google Scholar.
    Automatic CAPTCHA detection and resolution prompt.
    Log the download process and handle errors gracefully.
    Theme customization for the interface.
    Retry mechanism for downloading papers.

Installation

Prerequisites

    Python 3.x
    Pip (Python package installer)
    Google Chrome browser

Dependencies

Install the required Python packages using the following command:

pip install requests selenium beautifulsoup4 PyMuPDF tkinter

ChromeDriver

Download the appropriate version of ChromeDriver for your Chrome browser from here (https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the ./driver/ directory.

Usage

    Clone this repository to your local machine.

    Run the main script:

    python main.py

    Use the GUI to specify the search query, number of papers to download, and the save path.

    Click "Start Download" to begin the process.

GUI Elements

    Save Path: Directory where downloaded papers will be saved.
    Search Query: Query for searching papers on Google Scholar.
    Number of Papers: Number of papers to download.
    Start Download: Button to start the download process.
    CAPTCHA Resolved: Button to click after resolving a CAPTCHA manually.

Configuration

Themes

You can change the theme of the interface using the "Theme" menu:

    Floral Theme: A dark theme with floral colors.
    Default Theme: The default light theme.

Troubleshooting

Common Issues

    CAPTCHA Detected: The tool may detect a CAPTCHA. Solve it manually in the browser and then click "CAPTCHA Resolved".
    Corrupted PDFs: If a downloaded PDF is corrupted, it will be logged and removed. The tool will attempt to download the next paper.

Logs

The log area displays messages about the download process, including errors and successful downloads.

Disclaimer

This tool is intended for legal and ethical usage only. It is designed to assist in academic research for master's students and researchers. The developers are not responsible for any misuse of the tool.