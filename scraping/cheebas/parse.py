from lxml import html


def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//h4[contains(@class, "title")]')[0].text]
    
    prices = []
    price_table = tree.xpath('//table[@class="table table-bordered table-hover"]')
    if tree.xpath('//li[text()="Availability: Out of Stock"]'):
        prices.append(("", "out of stock"))
    elif price_table:
        price_values = price_table[0].xpath('./tr/td')
        for price_value in price_values:
            quantity = price_value.xpath('.//b')[0].text
            price = price_value.xpath('.//br')[0].tail.strip()
            price = price.replace("/g", "")
            price = float(price.replace("$", ""))
            
            if quantity == "Quarter":
                price = price * 7
            elif quantity == "Half":
                price = price * 14
            if quantity == "Ounce":
                price = price * 28
            
            prices.append((quantity, price))

    else:
        price = tree.xpath('//h2[@id="total_price"]')[0].text
        prices.append(("", price))
        
    product['prices'] = prices
    return product