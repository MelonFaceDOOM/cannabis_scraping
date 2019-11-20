from lxml import html
import json
import requests

#this site checks headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# get all product page links
page = requests.get("https://weed-deals.ca/shop/", headers=headers)
tree = html.fromstring(page.content)

product_urls = []
next_button = True
while next_button:
    for product in tree.xpath('//li[contains(@class, "product-grid-view")]'):
        product_urls.append(product.xpath('.//h3[@class="product-title"]//a')[0].attrib['href'])

    # check for next page button. If it exists, go to url associated with it
    # todo: should probably wrap this whole thing in a while loop that finishes when there is no next button

    next_button = tree.xpath('//a[@class="next page-numbers"]')
    if next_button:
        url = next_button[0].attrib['href']
        page = requests.get(url, headers=headers)
        tree = html.fromstring(page.content)
        
page_data=[]
for url in product_urls:
    page = requests.get(url, headers=headers)
    page_data.append([url, page.text])

with open("weed-deals_scraped.txt", "w") as f:
    json.dump(page_data, f)