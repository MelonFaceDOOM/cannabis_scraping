from lxml import html
import json
import requests

product_urls = []
page = requests.get("https://www.kingtuts.ca/shop/")
tree = html.fromstring(page.content)
for product in tree.xpath('//div[contains(@class, "type-product")]'):
    product_urls.append(product.xpath('.//p[@class="name product-title"]//a')[0].attrib['href'])
    
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("kingtuts_scraped.txt", "w") as f:
    json.dump(page_data, f)