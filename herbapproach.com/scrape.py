from lxml import html
import json
import requests

# get all product page links
page = requests.get("https://herbapproach.com/shop/")
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//div[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//p[@class="name product-title"]//a')[0].attrib['href'])

    next_button = tree.xpath('//a[@class="next page-number"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("herbapproach_scraped.txt", "w") as f:
    json.dump(page_data, f)