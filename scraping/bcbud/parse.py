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
    
    categories = []
    for category in tree.xpath('//span[@class="posted_in"]/a'):
        categories.append(category.text)
    product['categories'] = categories
    
    prices = []
    price_values = tree.xpath('//div[@class="row"]//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]')  
    # check if there is a single price for the listing
    if len(price_values) == 1:
        prices.append(("", float(price_values[0].xpath('./span')[0].tail)))
    else:
        # multiple prices may indicate a price-per gram scenario, or something else.
        # get the form and try to extract gram/dollar values
        start_pos = page_text.find('<form class="variations_form cart"')
        end_pos = page_text.find(">", start_pos)
        multipart_form = page_text[start_pos:end_pos+1]
        if multipart_form.find("3-5-grams") > 0:
            for gram_value in ["3-5-grams", "7-grams", "14-grams", "28-grams"]:
                gram_price = extract_gram_price(multipart_form, gram_value)
                prices.append((gram_value, gram_price))
        else:
            prices.append(("", "{} - {}".format(price_values[0].xpath('./span')[0].tail,
                                               price_values[1].xpath('./span')[0].tail)))
    product['prices'] = prices
    
    return product
 