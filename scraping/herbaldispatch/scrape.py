from lxml import html
import json
import requests

# get all product page links
page = requests.get("https://herbaldispatch.com/shop/")
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//li[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//h3[@class="product_title"]//a')[0].attrib['href'])

    next_button = tree.xpath('//a[@class="next page-numbers"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("herbaldispatch_scraped.txt", "w") as f:
    json.dump(page_data, f)