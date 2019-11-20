import json
from lxml import html
import csv 

with open(r'bcbud_scraped.txt', 'r') as f:
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
    
    categories = []
    for category in tree.xpath('//span[@class="posted_in"]/a'):
        categories.append(category.text)
    product['categories'] = categories
    
    prices = []
    price_values = tree.xpath('//div[@class="row"]//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]')  
    # check if there is a single price for the listing
    if len(price_values) == 1:
        prices.append(("", float(price_values[0].xpath('./span')[0].tail)))
    else:
        # multiple prices may indicate a price-per gram scenario, or something else.
        # get the form and try to extract gram/dollar values
        start_pos = page_text.find('<form class="variations_form cart"')
        end_pos = page_text.find(">", start_pos)
        multipart_form = page_text[start_pos:end_pos+1]
        if multipart_form.find("3-5-grams") > 0:
            for gram_value in ["3-5-grams", "7-grams", "14-grams", "28-grams"]:
                gram_price = extract_gram_price(multipart_form, gram_value)
                prices.append((gram_value, gram_price))
        else:
            prices.append(("", "{} - {}".format(price_values[0].xpath('./span')[0].tail,
                                               price_values[1].xpath('./span')[0].tail)))
    product['prices'] = prices
    products.append(product)
    
products_flattened = [["url", "name", "categories", "grams", "price"]]
for product in products:
    prices = product['prices']
    if prices:
        for price in prices:
            products_flattened.append([product['url'], product['name'], ", ".join(product['categories']), 
                                       price[0], price[1]])
    else:
        products_flattened.append([product['url'], product['name'], product['category'], 
                                       ""])

with open("bcbud_inventory.csv", "w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(products_flattened)