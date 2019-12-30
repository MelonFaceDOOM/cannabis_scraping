from lxml import html

    
def extract_price(tree):
    extracted_price = []
    
    table_text = tree.xpath('//div[@class="one"]//p')
    if table_text:
        table_text = table_text[0].text
        table_text = table_text.split("\n")
        for row in table_text:
            if row == "": #this catches some weirdly formatted tables on the site. I think it just makes sense to return 
                #empty list and handle them manually
                return []
            quantity, price = row.split("=")
            extracted_price.append((quantity,price))
        return extracted_price

    price_values = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span')
    if not price_values:
        extracted_price.append(("", tree.xpath('//p[@class="price"]/ins/span/span')[0].tail))
    else:
        price = "-".join([p.tail for p in price_values]) # 1 price will format as "25". two will format as "25-50"
        extracted_price.append(("", price))
    return extracted_price
    
    
def parse(html_raw):
    tree = html.fromstring(html_raw)
    if tree.xpath('//div[@class="et_password_protected_form"]'):
        return {'name': "password-protected", 'categories': [], 'prices': []}
        
    product = {}
    product['name'] = tree.xpath('//h1')[0].text
    product['prices'] = extract_price(tree)
    product['categories'] = [tree.xpath('//nav[@class="woocommerce-breadcrumb"]/a')[-1].text]
    return product