import os
import time
import base64
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from xvfbwrapper import Xvfb

# Set virtual display environment variable
os.environ["DISPLAY"] = ":99"

def scrape_interview_data(base_url, num_pages):
    vdisplay = Xvfb()
    vdisplay.start()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Ensure headless mode is used
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    chromedriver_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    
    interview_data = []
    
    for page_number in range(1, num_pages + 1):
        url = base_url.format(page_number)
        driver.get(url)
        time.sleep(3)  # Allow time for the page to load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        interview_list_container = soup.find('div', {'data-test': 'InterviewList'})
        if not interview_list_container:
            st.warning(f"No interviews found on page {page_number}")
            continue
        
        interview_containers = interview_list_container.find_all('div', class_='module-container_moduleContainer__tpBfv')
        
        for interview in interview_containers:
            interview_date = interview.find('span', class_='timestamp_reviewDate__dsF9n')
            interview_date = interview_date.get_text(strip=True) if interview_date else "N/A"
            
            role_applied_for = interview.find('h3', class_='heading_Heading__BqX5J')
            role_applied_for = role_applied_for.get_text(strip=True) if role_applied_for else "N/A"
            
            candidate_detail = interview.find('p', class_='interview-details_textStyle__gmhSJ')
            candidate_detail = candidate_detail.get_text(strip=True) if candidate_detail else "N/A"
            
            ratings = interview.find_all('div', class_='rating-icon_ratingContainer__9UoJ6')
            Offer = ratings[0].get_text(strip=True) if len(ratings) > 0 else "N/A"
            Experience = ratings[1].get_text(strip=True) if len(ratings) > 1 else "N/A"
            Difficulty = ratings[2].get_text(strip=True) if len(ratings) > 2 else "N/A"
            
            process = interview.find('div', class_='interview-details_interviewText__YH2ZO')
            process = process.get_text(strip=True) if process else "N/A"
            
            question = interview.find('div', class_='interview-details_interviewText__YH2ZO')
            question = question.get_text(strip=True) if question else "N/A"
            
            interview_data.append([interview_date, role_applied_for, candidate_detail, Offer, Experience, Difficulty, process, question])
    
    driver.quit()
    vdisplay.stop()
    return interview_data


def main():
    st.title("Glassdoor Interview Scraper")
    
    base_url = st.text_input("Enter the Company Interviews page base URL:", "https://www.glassdoor.co.in/Interview/Tata-Consultancy-Services-Interview-Questions-E13461.htm")
    num_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, max_value=111, value=1, step=1)
    base_url = base_url.replace(".htm", "_P{}.htm")
    
    if st.button("Scrape Interview Data"):
        st.write("Scraping data...")
        interview_data = scrape_interview_data(base_url, num_pages)
        
        if not interview_data:
            st.error("No interview data found. Try a different URL or increase the page count.")
            return
        
        df = pd.DataFrame(interview_data, columns=['Interview Date', 'Role Applied For', 'Candidate Detail', 'Offer', 'Experience', 'Difficulty', 'Process', 'Questions Asked'])
        
        df.to_excel("output.xlsx", index=False)
        st.success("Data saved successfully!")
        st.markdown(get_download_link('output.xlsx', 'Download Excel file'), unsafe_allow_html=True)


def get_download_link(file_path, text):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        return f'<a href="data:file/xlsx;base64,{b64}" download="{file_path}">{text}</a>'
    except FileNotFoundError:
        return "File not found."


if __name__ == "__main__":
    main()
