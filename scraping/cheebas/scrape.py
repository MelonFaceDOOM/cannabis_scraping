from lxml import html
import json
import requests
page = requests.get("https://cheebas.ca")
tree = html.fromstring(page.content)

def cheebify(subdirectory):
    subdirectory = subdirectory.strip("/")
    url = "https://cheebas.ca/" + subdirectory
    return url

# since there is no single shop page, we need to first get the url for 
# each of the category pages
categories = tree.xpath('//*[@id="horizontalmenu"]/ul/li[1]/ul/li/a')
category_urls = []
for p in products_menu:
    url = p.attrib['href']
    url = cheebify(url)
    category_urls.append(url)
  
# visit categories and get page urls. Everything is on one page,
# no page nav needed
product_urls = []
for category_url in category_urls:
    page = requests.get(category_url)
    tree = html.fromstring(page.content)
    
    for product in tree.xpath('//div[contains(@class, "product-layout")]//a'):
        url = product.attrib['href']
        url = cheebify(url)
        product_urls.append(url)

# save
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("cheebas_scraped.txt", "w") as f:
    json.dump(page_data, f)