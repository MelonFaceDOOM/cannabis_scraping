from lxml import html

def clean_price(raw):
    quantity = raw.split(" for ")[0]
    price = raw.split(" for ")[1]
    return quantity, price
    
    
def get_price_block(tree):
    # may be price block or just general information
    try:
        product_excerpt = tree.xpath('//div[@class="product-short-description"]')[0]
    except IndexError:
        return None
    
    for p in product_excerpt.xpath('./p'):
        if str(html.tostring(p)).find("for $") > -1:
            return p      
    return None
    
    
def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1[@class="product-title product_title entry-title"]')[0].text.strip()
    product['categories'] = [element.text for element in tree.xpath('//span[@class="posted_in"]/a')]
    
    price_block = get_price_block(tree)
    if price_block:
        prices = [p.strip() for p in price_block.xpath('./text()')]
        product['prices'] = [clean_price(price) for price in prices if price.find("for $") > -1]
        
    else:
        product['prices'] = []
        price_value = tree.xpath('//p/span[@class="woocommerce-Price-amount amount"]/span') or \
            tree.xpath('//p/ins/span[@class="woocommerce-Price-amount amount"]/span')
        
        product['prices'].append(("",price_value[0].tail))
            
    return product