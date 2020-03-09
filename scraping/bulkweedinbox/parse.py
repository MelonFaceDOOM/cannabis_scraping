from lxml import html


def extract_gram_price(form, gram_text):    
    start_pos = form.find(gram_text)
    if start_pos == -1:
        return None
    p1 = form[start_pos:]
    p2 = p1[p1.find("display_price&quot;:")+len("display_price&quot;:"):]
    try:
        extracted_price = float(p2[:p2.find(",")])
        return extracted_price
    except:
        return None

def parse(html_raw):
    tree = html.fromstring(html_raw)
    if tree.xpath('//form[@class="post-password-form"]'):
        return {'name': "password-protected", 'categories': [], 'prices': []}
    
    product = {}
    page_text = html_raw
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//div[@class="breadcrumbs-container"]/a')[-1].text]
    
    prices = []
    start_pos = page_text.find('<form class="variations_form cart')
    end_pos = page_text.find(">", start_pos)
    multipart_form = page_text[start_pos:end_pos+1]

    for gram_value in ["14 grams", "1-ounce", "1 ounce", "Ounce", "quarter-pound", "half-pound", "Half-Pound", "pound"]:
        gram_price = extract_gram_price(multipart_form, gram_value)
        if gram_price:
            prices.append((gram_value, gram_price))

    out_of_stock = tree.xpath('//p[@class="availability stock out-of-stock"]')
    if out_of_stock:
        prices.append(("", "out of stock"))
            
    if not prices:
        price_values = tree.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/span')
        if not price_values:
            prices.append(("", tree.xpath('//p[@class="price"]/ins/span/span')[0].tail))
        else:
            price = "-".join([p.tail for p in price_values]) # 1 price will format as "25". two will format as "25-50"
            prices.append(("", price))
    product['prices'] = prices
    return product
