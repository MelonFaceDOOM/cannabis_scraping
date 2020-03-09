from lxml import html
import json
import requests
from selenium import webdriver
from time import sleep

# this site checks for headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

page = requests.get("https://bulkweedinbox.com/shop", headers=headers)
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//section[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//h3[@class="heading-title product-name"]//a')[0].attrib['href'])
    
    next_button = tree.xpath('//a[@class="next page-numbers"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
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