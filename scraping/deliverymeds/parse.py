from lxml import html


def extract_gram_prices(form):    
    prices = []
    while True:
        # the weight/price values could be stored in several attribute names, so each has to be searched
        attribute_texts = ['attribute_pa_amount']
        for attribute_text in attribute_texts:
            start_pos = form.find(attribute_text)
            # break out of the attribute list search once the correct one has been identified
            if start_pos > -1:
                break
        
        # quit if no attribute values were found
        if start_pos == -1:
            break
            
        form = form[start_pos+len(f"{attribute_text}&quot;:&quot;"):]
        quantity = form[:form.find("&")]
        form = form[form.find("display_price&quot;:")+len("display_price&quot;:"):]
        price = form[:form.find(",")]
        prices.append((quantity, price))
    return prices

    
def get_multipart_form(page_text):
    start_pos = page_text.find('<form class="variations_form cart')
    if start_pos == -1:
        return None
    end_pos = page_text.find(">", start_pos)
    multipart_form = page_text[start_pos:end_pos+1]
    return multipart_form
    
    
def parse(html_raw):
    product = {}
    tree = html.fromstring(html_raw)
    product['name'] = tree.xpath('//h1')[0].text.strip()
    product['categories'] = [tree.xpath('//span[@class="posted_in"]/a')[0].text]
    
    product['prices'] = []
    multipart_form = get_multipart_form(html_raw)
    if multipart_form:
        product['prices'] = extract_gram_prices(multipart_form)
        
    # either there was no form or gram values weren't found in the form
    if not product['prices']:
        price_values = tree.xpath('//p/span[@class="woocommerce-Price-amount amount"]/span') or \
            tree.xpath('//p/ins/span[@class="woocommerce-Price-amount amount"]/span')
        
        if len(price_values) == 0:
            product['prices'].append(("", None))
        elif len(price_values) == 1:
            price = price_values[0].tail
            # a lot of cannabis products just have 1 price per gram on this site
            # just making everything have a weigh of 1g will cause inaccuracies for things like
            # vapes, but there's no reliable way to check to see if the product is cannabis
            # since they aren't categorized perfectly. It's easy to ignore the false-positives
            # in the future.
            product['prices'].append(("1 g", price))
        elif len(price_values) == 2:
            price = price_values[0].tail + " - " + price_values[1].tail
            product['prices'].append(("",price))
    return product
        