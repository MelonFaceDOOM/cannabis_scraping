#TODO: extract category information

import json

with open('greenace_scraped.txt', 'r') as f:
    page_data = json.load(f)
    
# this works for all but a couple pages. Looks like js interaction is needed on those pages, so the fastest
# solution will just be to go over those ones manually
def extract_price(tree):
    extracted_price = []
    1
    sale_indicator = tree.xpath('//p[@class="price"]//del')
    if sale_indicator:
        sale_price = tree.xpath('//p[@class="price"]//ins//span/span')[0].tail
        extracted_price.append(("",sale_price))
        return extracted_price

    prices = tree.xpath('//p[@class="price"]//span//span')
    if len(prices) == 1:
        extracted_price.append(("",prices[0].tail))
        return extracted_price
    
    price_table = tree.xpath('//div[@class="woocommerce-product-details__short-description"]')[0]
    for row in price_table.xpath('.//tr'):
        quantity = row.xpath('.//th')[0].text
        price = row.xpath('.//td')[0].text
        extracted_price.append((quantity,price))
    return extracted_price
    
for page in page_data:
    url = page[0]
    tree = html.fromstring(page[1])
    name = tree.xpath('//h1[@class="product_title entry-title"]')[0].text
    price = extract_price(tree)
    # todo: store this data somewhere
    # todo: find blanks and manually collect price data for these ones
    