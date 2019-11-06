from lxml import html
import json
import requests

product_urls = []
# just loop through page numbers until you hit 404 since this website doesn't have a next page button (infinite scrolling)
i = 1
while True:
    url = "https://www.thehighclub.ca/shop/page/{}".format(i)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    for product in tree.xpath('//li[contains(@class, "type-product")]'):
        product_urls.append(product.xpath('.//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')[0].attrib['href'])

    # check for next page button. If it exists, go to url associated with it
    # todo: should probably wrap this whole thing in a while loop that finishes when there is no next button

    error_404 = tree.xpath('//body[contains(@class, "error404")]')
    if error_404:
        break
        
    i += 1
    
page_data=[]
for url in product_urls:
    url = "https:" + url
    page = requests.get(url)
    page_data.append([url, page.text])

with open("thehighclub_scraped.txt", "w") as f:
    json.dump(page_data, f)