from lxml import html
import json
import requests
from selenium import webdriver

def ocsify(subdirectory):
    subdirectory = subdirectory.strip("/")
    url = "https://ocs.ca/" + subdirectory
    return url

# get all product page links
pages = ["https://ocs.ca/collections/all-cannabis-products?viewAll=false", "https://ocs.ca/collections/all-accessories?viewAll=false"]
product_urls = []
for p in pages:
    page = requests.get(p)
    tree = html.fromstring(page.content)

    next_button = True
    while next_button:
        for product in tree.xpath('//div[@class="product-tile__info"]'):
            url = product.xpath('.//div[@class="product-tile__data"]/a')[0].attrib['href']
            url = ocsify(url)
            product_urls.append(url)

        next_button = tree.xpath('//li[@class="pagination_next"]')
        if next_button:
            url = next_button[0].xpath('./a')[0].attrib['href']
            url = ocsify(url)
            page = requests.get(url)
            tree = html.fromstring(page.content)

chrome_path = r"C:\Users\JMILLER\AppData\Local\Programs\Python\Python35-32\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_path,options=chrome_options)
            
page_data=[]
for url in product_urls:
    driver.get(url)
    page = driver.page_source
    page_data.append([url, page])

with open("scraped.txt", "w") as f:
    json.dump(page_data, f)