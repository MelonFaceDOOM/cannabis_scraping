from lxml import html


def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//span[@class="posted_in"]/a')[0].text]
    
    if product['categories'] in ["Cannabis", "Concentrates", "Hash", "Kief"]:
        quantity = "1 gram"
    else:
        quantity = ""
        
    price = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span') or \
        tree.xpath('//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/span')
    product['prices'] = [(quantity, price[0].tail)]
    return product