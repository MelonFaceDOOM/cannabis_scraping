import json
from lxml import html
import csv 

with open(r'cheebas_scraped.txt', 'r') as f:
    page_data = json.load(f)
    
products = []
for page in page_data:
    product = {}
    page_text = page[1]
    tree = html.fromstring(page[1])
    product['url'] = page[0]
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['category'] = tree.xpath('//h4[contains(@class, "title")]')[0].text
    
    prices = []
    price_table = tree.xpath('//table[@class="table table-bordered table-hover"]')
    if tree.xpath('//li[text()="Availability: Out of Stock"]'):
        prices.append(("", "out of stock"))
    elif price_table:
        price_values = price_table[0].xpath('./tr/td')
        for price_value in price_values:
            quantity = price_value.xpath('.//b')[0].text
            price = price_value.xpath('.//br')[0].tail.strip()
            prices.append((quantity, price))

    else:
        price = tree.xpath('//h2[@id="total_price"]')[0].text
        prices.append(("", price))
        
    product['prices'] = prices
    products.append(product)

products_flattened = [["url", "name", "categories", "grams", "price"]]
for product in products:
    prices = product['prices']
    if prices:
        for price in prices:
            products_flattened.append([product['url'], product['name'], product['category'], 
                                       price[0], price[1]])
    else:
        products_flattened.append([product['url'], product['name'], product['category'], 
                                       ""])
                                   
with open("cheebas_inventory.csv", "w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(products_flattened)
