from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
import json
from tqdm import tqdm

chrome_options = Options()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless") #???
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="D:/tailieu/outProject/crawlJPF/chromedriver.exe")


def un_unicode(text):
    patterns = {
        'Nhân vật': '',
        'Series': '',
        'Hãng sản xuất': '',
        'Phát hành': '',
        'Kích thước': '',
        'Tỷ lệ': '',
        'Giá cập nhật tháng': '',
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y',
        '[\t\n\b]': '',
        '[\n]': ' ',
        '[:]': ''
    }
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def crawlPage(id, type, url):
    # url = "https://japanfigure.vn/collections/all"
    driver.get(url)
    # wait = WebDriverWait(driver, 0.05)

    # df_temp = pd.DataFrame(columns=[])
    #get ez info
    title_els = driver.find_element_by_xpath('//div[@class="product-title"]//h1')
    title = title_els.text
    # print(title)
    price_els = driver.find_element_by_xpath('//div[@class="product-price"]//span')
    price = price_els.text[:-1]
    # print(price)

    #get description
    description = ""
    desc = driver.find_elements_by_xpath('//div[@id="description2"]//p//span//span//span//span')
    # print("des len: ", len(desc))
    pub_key = "Hãng sản xuất"
    publisher = ""
    #get publisher and print shjt
    for des in desc:
        if pub_key in des.text:
            publisher = des.text[-16:]
            # print("publisher_bobo:", publisher)
        description = description + un_unicode(des.text) + ' '
    # print(description)

    # get tags
    # TODO need a function to handle tags
    df_tag = pd.DataFrame(columns=['id', 'tag_name'])
    tags_els = driver.find_elements_by_xpath('//ul[@class="tags"]//li//a')
    # print("tags number: ", len(tags_els))
    for tag in tags_els:
        s_tag = pd.Series([id, tag.text], index=['id', 'tag_name'])
        # print(s_tag)
        df_tag = df_tag.append(s_tag, ignore_index=True)
        description = description + tag.text + ' '
        # print(tag.text, end=', ')
    s_tag = pd.Series([id, type], index=['id', 'tag_name'])
    df_tag = df_tag.append(s_tag, ignore_index=True)
    description = description + type
    # print(df_tag)

    #get release date
    last_des = len(desc) - 1
    try:
        release_date = ''.join(c for c in str(desc[last_des].text) if c.isdigit() or c == '-' or c == '/')
    except:
        release_date = '2020'
    # print("release_date fuck:", release_date)

    #get image
    #TODO need function to handle image
    df_image = pd.DataFrame(columns=['id', 'url'])
    images_url = driver.find_elements_by_xpath("//div[@class='owl-item']//div//a")
    images_url = images_url + driver.find_elements_by_xpath("//div[@class='owl-item active']//div//a")
    # print("images len: ", len(images_url))
    for image_u in images_url:
        s_url = pd.Series([id, image_u.get_attribute('data-image')[2:]], index=['id', 'url'])
        df_image = df_image.append(s_url, ignore_index=True)
        # print(image_u.get_attribute('data-image'), end='\n')
    # print(df_image)

    names = ['id', 'title', 'price', 'release_date', 'quantity',
             'description', 'key_search']
    df_temp = pd.Series(index=names)
    df_temp['id'] = int(id)
    df_temp['title'] = title
    df_temp['price'] = price
    df_temp['release_date'] = release_date
    df_temp['quantity'] = 5
    df_temp['description'] = description.encode('utf-8').decode('latin-1')
    df_temp['key_search'] = un_unicode(description)
    # print("other:",df_temp)
    return df_temp, df_tag, df_image

def crawl_per_type(file_uri, id):
    with open(file_uri, 'r', encoding='utf-8') as f:
        links = json.load(f)
    type = f.name[5:-5]
    names = ['id', 'title', 'price', 'release_date', 'quantity',
                 'description', 'key_search']
    df_data_temp = pd.DataFrame(columns=names)
    df_tags = pd.DataFrame(columns=['id', 'tag_name'])
    df_image = pd.DataFrame(columns=['id', 'url'])

    for idx, link in zip(tqdm(range(len(links))), links[:]):
        # print(link)
        df_trip = crawlPage(id, type, str(link['item_href']))
        df_data_temp = df_data_temp.append(df_trip[0], ignore_index=True)
        df_tags = df_tags.append(df_trip[1], ignore_index=True)
        df_image = df_image.append(df_trip[2], ignore_index=True)
        id += 1
        # print('-------------')

    return df_data_temp, df_tags, df_image, id

id = 0
files = ['action-figure.json', 'scale-figure.json', 'chibi-figure.json']
# files = ['scale-figure.json']
# files = ['chibi-figure.json']
names = ['id', 'title', 'price', 'release_date', 'quantity',
                 'description', 'key_search']
df_data = pd.DataFrame(columns=names)
df_tags = pd.DataFrame(columns=['id', 'tag_name'])
df_image = pd.DataFrame(columns=['id', 'url'])

for file in files:
    print("crawling: ", file)
    df_data_temp, df_tags_temp, df_image_temp, id = crawl_per_type('data/'+file, id)
    # print("id after {}: ".format(file), id)
    df_data = df_data.append(df_data_temp, ignore_index=True)
    df_tags = df_tags.append(df_tags_temp, ignore_index=True)
    df_image = df_image.append(df_image_temp, ignore_index=True)
    print("---------------------------")

print("total crawl: {} and ID: {}".format(len(df_data), id))
df_data['id'] = pd.to_numeric(df_data['id'], downcast='integer')
# print(df_data.head())
df_data.to_csv('./data/data2.csv', encoding='utf-8', index=False)
df_tags.to_csv('./data/tags2.csv', encoding='utf-8', index=False)
df_image.to_csv('./data/images2.csv', encoding='utf-8', index=False)

driver.close()