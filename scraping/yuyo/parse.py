from lxml import html


def parse(html_raw):
    tree = html.fromstring(html_raw.encode('utf-8'))
    product = {}
    product['name'] = tree.xpath('//h1[@class="margin-t0 margin-b4"]')[0].text
    product['categories'] = [tree.xpath('//span[@class="bread-crumb last-bread-crumb"]')[0].text]

    product['prices'] = []
    price_table = tree.xpath('//table[@class="product_tier_pricing"]')
    if price_table:
        weights = price_table[0].xpath('./tr/th')
        weights = [weight.text for weight in weights]

        prices = price_table[0].xpath('./tr/td/span')
        prices = [price.text for price in prices]

        product['prices'] = list(zip(weights, prices))

    # either there was no form or gram values weren't found in the form
    if not product['prices']:
        product['prices'] = [("", tree.xpath('//span[@class="price-value"]/span')[0].text)]
        
    return product