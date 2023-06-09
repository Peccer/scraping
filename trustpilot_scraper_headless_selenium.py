# Scraping Trustpilot reviews with Selenium, in Deepnote (deepnote.com, my favourite data analysis virtual notebook platform
!pip install selenium==4.9.0

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

!sudo apt-get update
!sudo apt-get install chromium-driver -y

options = Options()
options.add_argument('--headless')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
browser = Chrome(options=options)

import pandas as pd
import datetime as dt
import json
import pprint
import time

review_data = []

# Website to be scraped from trustpilot. Make sure to double check if the value matches the actual trustpilot url
website_scrape = "catawiki.com"

# Set Trustpilot page numbers to scrape here
from_page = 1
to_page = 100

delay = 3

for i in range(from_page, to_page + 1):
    # print(i)
    if i == 1:
        url = f"https://nl.trustpilot.com/review/{website_scrape}?languages=all&sort=recency"
    else:
        i = str(i)
        url = f"https://nl.trustpilot.com/review/{website_scrape}?date=last6months&languages=all&page={i}&sort=recency"
    
    # print(url)
    
    browser.get(url)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, '__NEXT_DATA__')))
        print(f'Page {i} is ready')
    except TimeoutException:
        print("Loading took too much time!")
    web_page = browser.page_source
    soup = BeautifulSoup(web_page, "html.parser")
    try:
        data = json.loads(soup.find('script', type='application/json', id="__NEXT_DATA__").text)
    except:
        print("could not load data")
        pass
    reviews = data["props"]["pageProps"]["reviews"]
    review_data.append(reviews)
    
    
    # flatten data
    flat_list = [item for sublist in review_data for item in sublist]
    
    #flattened data to dataframe
    df = pd.json_normalize(flat_list)
    
    # drop duplicates
    df = df.loc[df.astype(str).drop_duplicates().index]
    #print(df.info())
    
    # Save to CSV
    df.to_csv("filenamehere.csv",index=False)
    # df["str_length_text"] = df["text"].str.len()
