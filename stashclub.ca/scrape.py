from selenium import webdriver
import json

#chrome_path = r"C:\Users\JMILLER\AppData\Local\Programs\Python\Python35-32\chromedriver.exe"
chrome_path = r"C:\Users\Jacob\AppData\Local\Programs\Python\Python37\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

product_urls = []
for i in range(1,18):
    driver.get("https://stashclub.ca/shop/page/{}/".format(i))
    for product in driver.find_elements_by_xpath('//a[@class="woocommerce-loop-product__link"]'):
        product_urls.append(product.get_attribute('href'))
        
page_data=[]
for url in product_urls:
    driver.get(url)
    page = driver.page_source
    page_data.append(page)

with open("stashclub_scraped.txt", "w") as f:
    json.dump(page_data, f)