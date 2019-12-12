from lxml import html
import re


def get_price_block(tree):
    # price info will be in a ul within the description, but there can be multiple uls in varying orders
    # therefore, it's easiest to find the p element with the text "pricing"
    # the ul with the prices always follows this p element
    
    price_desc = tree.xpath('//div[@class="woocommerce-product-details__short-description"]')
    if not price_desc:
        return None
    titles = price_desc[0].xpath('./p')
    price_title = None
    for title in titles:
        #find the p element with the word "pricing"
        if str(html.tostring(title)).find("pricing") > -1:
            price_title=title
    
    if not price_title:
        return None
    
    price_block = price_title.getnext()
    return price_block

    
def get_raw_prices(price_block):
    prices = price_block.xpath('./li/span') or price_block.xpath('./li') 
    prices = [p.text.split("=")[0] for p in prices if p.text]
    
    # if no text was found in the above elements, it could be because there is a sale and the price follows a del element
    if not prices:
        prices = price_block.xpath('./li/del')
        prices = [p.tail.split("=")[0] for p in prices if p.tail]
    return prices


def clean_price(raw):
    quantity_pattern = "([.\d]+)( [Gg]rams?|$)"
    price_pattern = "\$(\d+)"
    
    quantity = re.search(quantity_pattern, raw)
    price = re.search(price_pattern, raw)
    
    if not quantity or not price:
        return None
    
    return quantity.group(1) + quantity.group(2), price.group(1)

    
def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    
    categories = tree.xpath('//span[@class="posted_in"]/a')
    categories = [c.text for c in categories]
    product['categories'] = categories
    
    price_values = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span') or \
            tree.xpath('//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/span')
    price_block = get_price_block(tree)
    if len(price_values) == 2 and price_block:
        raw_prices = get_raw_prices(price_block)
        product['prices'] = [clean_price(p) for p in raw_prices if clean_price(p)]
    elif len(price_values) == 2 and not price_block:
        product['prices'] = [("", price_values[0].tail), ("", price_values[1].tail)]
    else:
        product['prices'] = [("", price_values[0].tail)]
    
    return product