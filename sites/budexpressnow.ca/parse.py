import json
from lxml import html
import csv 

with open(r'budexpressnow_scraped.txt', 'r') as f:
    page_data = json.load(f)
    
def extract_gram_price(form, gram_text):    
    start_pos = form.find(gram_text)
    if start_pos == -1:
        return None
    p1 = form[start_pos:]
    p2 = p1[p1.find("display_price&quot;:")+len("display_price&quot;:"):]
    return float(p2[:p2.find(",")])

products=[]
for page in page_data:
    product = {}
    
    page_text = page[1]
    tree = html.fromstring(page[1])
    product['url'] = page[0]
    product['name'] = tree.xpath('//h1')[0].text.strip()

    product['category'] = tree.xpath('//div[@class="summary entry-summary"]/nav/a')[-1].text
    
    prices = []
    
    start_pos = page_text.find('<form class="variations_form cart')
    end_pos = page_text.find(">", start_pos)
    multipart_form = page_text[start_pos:end_pos+1]

    for gram_value in ["1-gram", "3-5-grams", "7-grams", "14-grams", "28-grams"]:
        gram_price = extract_gram_price(multipart_form, gram_value)
        if gram_price:
            prices.append((gram_value, gram_price))

    out_of_stock = tree.xpath('//p[@class="stock out-of-stock"]')
    if out_of_stock:
        prices.append(("", "out of stock"))
            
    if not prices:
        price_values = tree.xpath('//div[@class="subtitle-price"]/span[@class="woocommerce-Price-amount amount"]/span')
        if not price_values:
            prices.append(("", tree.xpath('//div[@class="subtitle-price"]/ins/span/span')[0].tail))
        else:
            price = "-".join([p.tail for p in price_values]) # 1 price will format as "25". two will format as "25-50"
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
                                   
            
with open("budexpressnow_inventory.csv", "w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(products_flattened)