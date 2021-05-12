from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="D:/tailieu/outProject/crawlJPF/chromedriver.exe")

def crawlType(data, url):
    # url = "https://japanfigure.vn/collections/all"
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    for i in range(0,300):
        try:
            driver.execute_script("document.getElementsByClassName('btn-loading')[0].click()")
            time.sleep(0.3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except:
            break;

    # title = driver.find_elements_by_xpath("//*[@class='product-lists']"
    #                                       "//*[@class='product-wrapper']"
    #                                       "//*[@class='product-information']"
    #                                       "//*[@class='product-detail']"
    #                                       "//*[@class='product-info']"
    #                                       "//*[@class='product-title']"
    #                                       "//a")
    title = driver.find_elements_by_xpath('//h2[@class="product-title name"]')

    print("num of items:", len(title))

    for browse in title:
        text = browse.find_element_by_xpath(".//a").get_attribute('href')
        data.append({"item_href" : text})
    print(len(data))


with open('data/type.json', 'r', encoding='latin-1') as f:
    links = json.load(f)

for link in links:
    data = []
    crawlType(data, link['type_url'])
    df = pd.DataFrame(data).to_json('./data/'+link['type_name']+'.json', orient='records')


driver.close()