#TODO: extract category information

import json
from lxml import html

with open(r'buymyweedonline.ca\buymyweedonline_scraped.txt', 'r') as f:
    page_data = json.load(f)
    
def extract_price(tree):
    extracted_price = []
    
    sale_indicator = tree.xpath('//p[@class="price"]//del')
    if sale_indicator:
        sale_price = tree.xpath('//p[@class="price"]//ins//span/span')[0].tail
        extracted_price.append(("",sale_price))
        return extracted_price

    prices = tree.xpath('//p[@class="price"]//span//span')
    if len(prices) == 1:
        extracted_price.append(("",prices[0].tail))
        return extracted_price
    
    table_text = tree.xpath('//div[@class="one"]//p')
    if not table_text:
        return None
    table_text = table_text[0].text
    table_text = table_text.split("\n")
    for row in table_text:
        if row == "": #this catches some weirdly formatted tables on the site. I think it just makes sense to return 
            #None and handle them manually
            return None
        quantity, price = row.split("=")
        extracted_price.append((quantity,price))
    return extracted_price
    
for page in page_data:
    url = page[0]
    tree = html.fromstring(page[1])
    name = tree.xpath('//h1')[0].text
    price = extract_price(tree)
    print(name)
    # todo: store this data somewhere
    # todo: find blanks and manually collect price data for these ones
    