import os
import time
import base64
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Function to scrape interview data from Glassdoor
def scrape_interview_data(base_url, num_pages):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--remote-debugging-port=9222")  # Required for headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Required for cloud environments

    # Specify the path to ChromeDriver in Streamlit Cloud
    chromedriver_path = "/usr/bin/chromedriver"

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    interview_data = []

    for page_number in range(1, num_pages + 1):
        url = base_url.format(page_number)
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'lxml')

        interview_containers = soup.find_all('div', class_='mt-0 mb-0 my-md-std p-std gd-ui-module css-cup1a5 ec4dwm00')
        for interview in interview_containers:
            interview_date = interview.find('time').get_text() if interview.find('time') else "N/A"
            role_applied_for = interview.find('h2', class_='mt-0 mb-xxsm css-93svrw el6ke055').get_text() if interview.find('h2', class_='mt-0 mb-xxsm css-93svrw el6ke055') else "N/A"
            candidate_detail = interview.find('p', class_='mt-0 mb css-13r90be e1lscvyf1').get_text() if interview.find('p', class_='mt-0 mb css-13r90be e1lscvyf1') else "N/A"
            ratings = interview.find_all('span', class_="mb-xxsm")
            Offer = ratings[0].get_text() if len(ratings) > 0 else "N/A"
            Experience = ratings[1].get_text() if len(ratings) > 1 else "N/A"
            Difficulty = ratings[2].get_text() if len(ratings) > 2 else "N/A"
            application = interview.find('p', class_='mt-xsm mb-std').get_text() if interview.find('p', class_='mt-xsm mb-std') else "N/A"
            process_element = interview.find('p', class_='css-lyyc14 css-w00cnv mt-xsm mb-std')
            if not process_element:
                process_element = interview.find('p', class_='css-w00cnv mt-xsm mb-std')
            process = process_element.get_text() if process_element else "N/A"
            question = interview.find("span", class_="d-inline-block mb-sm").get_text() if interview.find("span", class_="d-inline-block mb-sm") else "N/A"
            interview_data.append([interview_date, role_applied_for, candidate_detail, Offer, Experience, Difficulty, application, process, question])

    driver.quit()
    return interview_data

# Main function to run the Streamlit app
def main():
    st.title("Glassdoor Interview Scraper")

    # Input fields for base URL and number of pages
    base_url = st.text_input("Enter the Company Interviews page base URL:", "https://www.glassdoor.co.in/Interview/Tata-Consultancy-Services-Interview-Questions-E13461.htm")
    num_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, max_value=111, value=10, step=1)
    base_url = base_url.replace(".htm", "_P{}.htm")

    # Button to trigger scraping
    if st.button("Scrape Interview Data"):
        st.write("Scraping data...")

        # Scrape interview data
        interview_data = scrape_interview_data(base_url, num_pages)

        # Convert data to DataFrame
        df = pd.DataFrame(interview_data, columns=['Interview Date', 'Role Applied For', 'Candidate Detail', 'Offer','Experience','Difficulty', 'Application', 'Process', 'Questions Asked'])

        # Save DataFrame to Excel and create download link
        with st.spinner("Saving data to Excel..."):
            df.to_excel('Company_interview_details.xlsx', index=False)
        
        st.success("Data saved successfully!")

        # Create download link for Excel file
        st.markdown(get_download_link('Company_interview_details.xlsx', 'Download Excel file'), unsafe_allow_html=True)

# Function to generate download link for files
def get_download_link(file_path, text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    href = f'<a href="data:file/xlsx;base64,{b64}" download="{file_path}">{text}</a>'
    return href

if __name__ == "__main__":
    main()