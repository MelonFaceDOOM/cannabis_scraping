from lxml import html

    
def extract_gram_price(form, gram_text):    
    start_pos = form.find(gram_text)
    if start_pos == -1:
        return None
    p1 = form[start_pos:]
    p2 = p1[p1.find("display_price&quot;:")+len("display_price&quot;:"):]
    return float(p2[:p2.find(",")])


def parse(html_raw):
    product = {}
    page_text = html_raw
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//div[@class="summary entry-summary"]/nav/a')[-1].text]
   
    prices = []
    start_pos = page_text.find('<form class="variations_form cart')
    end_pos = page_text.find(">", start_pos)
    multipart_form = page_text[start_pos:end_pos+1]

    for gram_value in ["1-gram", "3-5-grams", "7-grams", "14-grams", "28-grams"]:
        gram_price = extract_gram_price(multipart_form, gram_value)
        if gram_price:
            prices.append((gram_value, gram_price))

    out_of_stock = tree.xpath('//p[@class="stock out-of-stock"]')
    if out_of_stock:
        prices.append(("", "out of stock"))
            
    if not prices:
        price_values = tree.xpath('//div[@class="subtitle-price"]/span[@class="woocommerce-Price-amount amount"]/span')
        if not price_values:
            prices.append(("", tree.xpath('//div[@class="subtitle-price"]/ins/span/span')[0].tail))
        else:
            price = "-".join([p.tail for p in price_values]) # 1 price will format as "25". two will format as "25-50"
            prices.append(("", price))
    product['prices'] = prices
    
    return product
