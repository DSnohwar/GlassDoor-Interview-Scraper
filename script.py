# https://www.glassdoor.co.in/Interview/Tata-Consultancy-Services-Interview-Questions-E13461.htm
# https://www.scrapethissite.com/pages/simple/

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
params = {
    "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
}

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", params)

base_url = 'https://www.glassdoor.co.in/Interview/Tata-Consultancy-Services-Interview-Questions-E13461_P{}.htm'

# Iterating through each page of TCS interview questions
for page_number in range(1, 111):
    time.sleep(2)
    url = base_url.format(page_number)
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Extracting interview details from the page
    interview_data = []

    interview_containers = soup.find_all('div', class_='mt-0 mb-0 my-md-std p-std gd-ui-module css-cup1a5 ec4dwm00')
    for interview in interview_containers:
        # Interview date
        interview_date = interview.find('time').get_text()

        # Role applied for
        role_applied_for = interview.find('h2', class_='mt-0 mb-xxsm css-93svrw el6ke055').get_text()

        # Candidate detail
        candidate_detail = interview.find('p', class_='mt-0 mb css-13r90be e1lscvyf1').get_text()

        # Ratings
        ratings = interview.find_all('span', class_="mb-xxsm")
        Offer = ratings[0].get_text()
        Experience = ratings[1].get_text()
        Difficulty = ratings[2].get_text()

        # Application details
        application = interview.find('p', class_='mt-xsm mb-std').get_text()

        # Process
        process_element = interview.find('p', class_='css-lyyc14 css-w00cnv mt-xsm mb-std')
        if not process_element:
            process_element = interview.find('p', class_='css-w00cnv mt-xsm mb-std')
        process = process_element.get_text() if process_element else ""

        # Interview questions
        question = interview.find("span", class_="d-inline-block mb-sm").get_text() if interview.find("span", class_="d-inline-block mb-sm") else ""

        interview_data.append([interview_date, role_applied_for, candidate_detail, Offer, Experience, Difficulty, application, process, question])

    # Convert interview data to a DataFrame
    df = pd.DataFrame(interview_data, columns=['Interview Date', 'Role Applied For', 'Candidate Detail', 'Offer','Experience','Difficulty', 'Application', 'Process', 'Questions Asked'])

    # Check if the Excel file exists
    if os.path.exists('interview_details.xlsx'):
        existing_df = pd.read_excel('interview_details.xlsx',)
        df = pd.concat([existing_df, df], ignore_index=True)
        with pd.ExcelWriter('interview_details.xlsx', if_sheet_exists='replace', engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name='Sheet1',index=False)
    else:
        df.to_excel('interview_details.xlsx', index=False)

driver.quit()
