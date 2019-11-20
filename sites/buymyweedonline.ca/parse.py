import json
from lxml import html
import csv

with open(r'buymyweedonline_scraped.txt', 'r') as f:
    page_data = json.load(f)
    
def extract_price(tree):
    extracted_price = []
    
    table_text = tree.xpath('//div[@class="one"]//p')
    if table_text:
        table_text = table_text[0].text
        table_text = table_text.split("\n")
        for row in table_text:
            if row == "": #this catches some weirdly formatted tables on the site. I think it just makes sense to return 
                #None and handle them manually
                return None
            quantity, price = row.split("=")
            extracted_price.append((quantity,price))
        return extracted_price

    price_values = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span')
    if not price_values:
        extracted_price.append(("", tree.xpath('//p[@class="price"]/ins/span/span')[0].tail))
    else:
        price = "-".join([p.tail for p in price_values]) # 1 price will format as "25". two will format as "25-50"
        extracted_price.append(("", price))
    return extracted_price
    
products = []
for page in page_data:
    tree = html.fromstring(page[1])
    
    if tree.xpath('//div[@class="et_password_protected_form"]'):
        continue
        
    product = {}
    product['url'] = page[0]
    product['name'] = tree.xpath('//h1')[0].text
    product['prices'] = extract_price(tree)
    product['category'] = tree.xpath('//nav[@class="woocommerce-breadcrumb"]/a')[-1].text
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
                                   
with open("buymyweedonline_inventory.csv", "w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(products_flattened)