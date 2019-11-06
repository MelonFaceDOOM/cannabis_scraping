from lxml import html
import json
import requests
from selenium import webdriver
from time import sleep

# this site checks for headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

page = requests.get("https://bulkweedinbox.com/product-category/accessories/", headers=headers)
tree = html.fromstring(page.content)

categories = tree.xpath('//ul[@class="product-categories"]')[0]
category_urls = []
for category in categories:
    url = category.xpath('.//a')[0].attrib['href']
    category_urls.append(url)

product_urls = []
for url in category_urls:
    # get all product page links
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)
    
    for product in tree.xpath('//section[contains(@class, "wvs-pro-product")]'):
        product_urls.append(product.xpath('.//h3[@class="heading-title product-name"]//a')[0].attrib['href'])

# need selenium to get past cloudflare check. Just load one page,
# let 5 second test pass, then you can loop through everything else without waiting
chrome_path = r"C:\Users\JMILLER\AppData\Local\Programs\Python\Python35-32\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
driver.get("https://bulkweedinbox.com/product/a-boveda-packs-67-grams/")
sleep(10)

page_data=[]
for url in product_urls:
    driver.get(url)
    page = driver.page_source
    page_data.append([url, page])
    
with open("bulkweedinbox_scraped.txt", "w") as f:
    json.dump(page_data, f)