import json
from lxml import html
import csv 

with open(r'deliverymeds_scraped.txt', 'r') as f:
    page_data = json.load(f)

products = []
for page in page_data:
    product = {}
    page_text = page[1]
    tree = html.fromstring(page[1])
    product['url'] = page[0]
    product['name'] = tree.xpath('//h1')[0].text.strip()
    
    product['category'] = tree.xpath('//span[@class="posted_in"]/a')[0].text
    
    if product['category'] in ["Cannabis", "Concentrates", "Hash", "Kief"]:
        quantity = "1 gram"
    else:
        quantity = ""
        
    price = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span') or \
        tree.xpath('//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/span')
    product['price'] = (quantity, price[0].tail)
    products.append(product)
    
products_flattened = [["url", "name", "categories", "grams", "price"]]
for product in products:
    products_flattened.append([product['url'], product['name'], product['category'], product['price'][0], product['price'][1]])

with open("deliverymeds_inventory.csv", "w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(products_flattened)