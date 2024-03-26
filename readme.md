# Glassdoor Interview Scraper

This project scrapes interview data from Glassdoor using Selenium and BeautifulSoup, and saves the data to an Excel file. The project also includes a Streamlit app for a user-friendly interface.

## Files

- `app.py`: This is the main file that runs the Streamlit app. It includes functions to scrape interview data from Glassdoor and generate a download link for the scraped data.
- `script.py`: This script scrapes interview data from a specified Glassdoor page and saves the data to a pandas DataFrame.
- `Company_interview_details.xlsx`: This Excel file contains the scraped interview data.
- `Extracted data/`: This directory contains additional Excel files with interview data.
- `glassdoor_page.html`: This HTML file is a saved Glassdoor page.
- `requirements.txt`: This file lists the Python libraries required for this project.

## Installation

To install the required libraries, run the following command:

```sh
pip install -r requirements.txt
```

## Usage

```sh
streamlit run app.py
```