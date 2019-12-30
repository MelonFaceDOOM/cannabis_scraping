from lxml import html


def get_price_block(tree):
    # may be price block or just general information
    try:
        price_block = tree.xpath('//table[@class="shop_attributes"]')[0]
    except IndexError:
        return None
    block_text = str(html.tostring(price_block))
    if block_text.find("$") > -1:
        return price_block
    else:
        return None

        
def get_prices(price_block):
    prices = []
    # this gets convoluted because there can be a table with rows. the cells can be bolded. 
    # the cells can also have del tags if there's a sale
    # this could only be clean if i wrote things like, for example, something that checks a tag and also checks 
    # for a del child's tail
    # may be worthwhile since the same thing will come up in other stores as well
    for row in price_block.xpath('./tbody/tr'):
        quantity = row.xpath('./th')[0].text
        price = row.xpath('./td')[0].text
        if not price:
            if row.xpath('./td/strong'):
                price = row.xpath('./td/strong')[0].text
                if not price:
                    price = row.xpath('./td/strong/del')[0].tail
        if not price:
            price = row.xpath('./td/del')[0].tail
        if quantity and price:
            prices.append((quantity, price))
    return prices

    
def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//nav[@class="woocommerce-breadcrumb breadcrumbs"]/a')[-1].text]

    price_values = tree.xpath('//p/span[@class="woocommerce-Price-amount amount"]/span') or \
            tree.xpath('//p/ins/span[@class="woocommerce-Price-amount amount"]/span')
    
    price_block = get_price_block(tree)
    if price_block:
        prices = get_prices(price_block)
    else:
        prices = []
        for price_value in price_values:
            prices.append(("", price_value.tail))
    product['prices'] = prices
    return product