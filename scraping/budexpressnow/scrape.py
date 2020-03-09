from lxml import html
import json
import requests

product_urls = []
i = 0
# There are no page buttons, and the site has infinite scrolling
# luckily, just adding "page/#" to the url will paginate results appropriately
# I just looped through page numbers until I hit their 'page not found' page
while True:
    i+=1
    page = requests.get("https://www.budexpressnow.ca/shop/page/{}".format(i))
    tree = html.fromstring(page.content)
    
    page_not_found = tree.xpath('//h2[contains(text(), "Page not found")]')
    if page_not_found:
        break
    
    for product in tree.xpath('//article[contains(@class, "product-item")]'):
        product_urls.append(product.xpath('.//a[@class="product-item__title"]')[0].attrib['href'])
        
page_data=[]
for url in product_urls:
    page = requests.get(url)
    page_data.append([url, page.text])

with open("budexpressnow_scraped.txt", "w") as f:
    json.dump(page_data, f)