from lxml import html

def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [element.text for element in tree.xpath('//span[@class="posted_in"]/a')]
    
    price_values = tree.xpath('//p/span[@class="woocommerce-Price-amount amount"]') or \
        tree.xpath('//p/ins/span[@class="woocommerce-Price-amount amount"]') or \
        tree.xpath('//p/span/span[@class="woocommerce-Price-amount amount"]') or \
        tree.xpath('//p/span/ins/span[@class="woocommerce-Price-amount amount"]')

    product['prices'] = []
    for p in price_values:
        price = p.xpath('./span')[0].tail
        quantity = p.tail
        quantity = quantity.strip(' /') if quantity else ""
        product['prices'].append((quantity, price))
        
    return product