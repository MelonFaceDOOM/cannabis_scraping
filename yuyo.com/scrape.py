from lxml import html
import json
import requests

def yuyoify(subdirectory):
    subdirectory = subdirectory.strip("/")
    url = "https://yuyo.com/" + subdirectory
    return url

# easier to just grab the categories manually than try to extract
category_urls = [
    "https://www.yuyo.com/strains/",
    "https://www.yuyo.com/cbd/",
    "https://www.yuyo.com/edibles/",
    "https://www.yuyo.com/concentrates/",
    "https://www.yuyo.com/vapes/"
]

product_urls = []
next_button = True
for url in category_urls:
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    for product in tree.xpath('//div[@class="material_wrapper item"]'):
        product_url = yuyoify(product.xpath('.//a[@class="product-title"]')[0].attrib['href'])
        product_urls.append(product_url)
        
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("yuyo_scraped.txt", "w") as f:
    json.dump(page_data, f)