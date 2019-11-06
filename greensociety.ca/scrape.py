from lxml import html
import json
import requests
from selenium import webdriver
from time import sleep

chrome_path = r"C:\Users\JMILLER\AppData\Local\Programs\Python\Python35-32\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
driver.get("https://www.greensociety.ca/shop/")

category_urls = []
categories = driver.find_elements_by_xpath("//ul[@class='product-categories']/li/a")
for c in categories:
    category_urls.append(c.get_attribute("href"))
    
product_urls = []
for url in category_urls:
    driver.get(url)
    next_page = True
    while next_page:
        products = driver.find_elements_by_xpath('//div[contains(@class, "type-product")]')
        for p in products:
            product_url = p.find_element_by_xpath('.//p[@class="name product-title"]/a').get_attribute("href")
            product_urls.append(product_url)
        
        next_page = driver.find_elements_by_xpath('//a[@class="next page-number"]')
        if next_page:
            driver.get(next_page[0].get_attribute("href"))
            
page_data=[]
for url in product_urls:
    driver.get(url)
    page = driver.page_source
    page_data.append([url, page])
    
with open("greensociety_scraped.txt", "w") as f:
    json.dump(page_data, f)