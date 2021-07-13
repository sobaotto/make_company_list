import requests
import os
import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import urllib.request
import pandas as pd
import time
import numpy as np

# launch chrome browser
driver = webdriver.Chrome()

master_url = "~~~~~"
urls = []

driver.get(master_url)
while True:
    time.sleep(1)
    current_url = driver.current_url
    html = requests.get(current_url)
    bs = BeautifulSoup(html.content, 'lxml')

    projects_elem = bs.select('[class="projects-index-list"]')

    for link_elem in projects_elem[0].find_all(class_="project-title"):
        link = "https://www.~~~~~~.com/" + link_elem.find("a").get('href')
        urls.append(link)

    # 次のリンクを取得しページ遷移
    try:
        next_btn_elem = driver.find_element_by_link_text("次へ")
        next_btn_elem.click()
    except:
        print("終わり")
        driver.quit()
        break

companies = []
company_info = {"name": "", "wantedly": "", "link": "",
                "established": "", "members": 0, "features": "", "location": ""}

driver = webdriver.Chrome()
for url in urls:
    # google image search
    time.sleep(1)
    driver.get(url)
    current_url = driver.current_url
    html = requests.get(current_url)

    bs = BeautifulSoup(html.content, 'lxml')

    company_elem = bs.select('[class="company"]')

    info_elems = company_elem[0].find_all('li')
    info_elems.insert(0, url)
    info_elems.insert(0, company_elem[0].find(class_='company-name'))
    for (elem, key) in zip(info_elems, company_info.keys()):
        try:
            company_info[key] = elem.text.replace('\n', "")
        except:
            company_info[key] = elem

    companies.append(company_info)
    company_info = {"name": "", "wantedly": "", "link": "",
                    "established": "", "members": 0, "features": "", "location": ""}

fruit_list = [('test', "test", 'test', "test", "test", "test")]
# Create a DataFrame object
df = pd.DataFrame(fruit_list, columns=[
                  "name", "link", "established", "members", "features", "location"])
# Add new ROW
for company in companies:
    df = df.append(company, ignore_index=True)
print(df)

df.to_excel("会社リスト.xlsx")

driver.quit()
