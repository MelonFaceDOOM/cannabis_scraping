from lxml import html

def parse(html_raw):
    tree = html.fromstring(html_raw)
    product = {}
    product['name'] = tree.xpath('//h1[@class="product__title h2"]')[0].text.strip()
    
    try:
        product['categories'] = [tree.xpath('//a[@class="breadcrumbs__collection"]')[0].text]
    except:
        product['categories'] = [] # some have no category
    
    product['prices'] = []
    
    # this may contain non-price/weight info.
    prices_and_weights = tree.xpath('//li[@class="swatch swatch--weight"]')
    
    for pw in prices_and_weights:
        price = pw.xpath('.//span[@class="swatch__price"]')
        if price: 
            price = price[0].text
            weight = pw.xpath('.//label[@class="swatch__label"]')[0].attrib['title']
            product['prices'].append((weight, price))
        
    # either there was no form or gram values weren't found in the form
    if not product['prices']:
        product['prices'].append(("", tree.xpath('//h2[@class="product__price"]')[0].text.strip()))
        
    return product