from lxml import html
import json
import requests

# get all product page links
page = requests.get("https://buymyweedonline.ca/shop-page/")
tree = html.fromstring(page.content)

product_urls = []
for product in tree.xpath('//li[contains(@class, "product")]'):
    url = product.xpath(".//a")[0].attrib['href']
    product_urls.append(url)
    
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("buymyweedonline_scraped.txt", "w") as f:
    json.dump(page_data, f)