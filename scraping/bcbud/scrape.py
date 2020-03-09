from lxml import html
import json
import requests

# this site checks for headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# get all product page links
page = requests.get("https://bcbud.store/shop/", headers=headers)
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//div[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//p[@class="product-title"]//a')[0].attrib['href'])

    next_button = tree.xpath('//a[@class="next page-numbers"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url, headers=headers)
        tree = html.fromstring(page.content)
        
page_data=[]
for url in product_urls:
    page = requests.get(url, headers=headers)
    page_data.append([url, page.text])

with open("bcbud.txt", "w") as f:
    json.dump(page_data, f)