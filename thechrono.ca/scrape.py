from lxml import html
import json
import requests

page = requests.get("https://www.thechrono.ca/shop/")
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//div[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')[0].attrib['href'])

    # check for next page button. If it exists, go to url associated with it
    # todo: should probably wrap this whole thing in a while loop that finishes when there is no next button

    next_button = tree.xpath('//a[@class="next page-numbers"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("thechrono_scraped.txt", "w") as f:
    json.dump(page_data, f)