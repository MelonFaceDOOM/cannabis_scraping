from lxml import html


def extract_gram_prices(form):    

    prices = []
    while True:
        # the weight/price values could be stored in several attribute names, so each has to be searched
        attribute_texts = ['attribute_choose-an-options', 'attribute_choose-an-option', 'attribute_choose-your-option',
                          'attribute_choose-options', 'attribute_your-options', 'attribute_pa_choose']
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


def find_multipart_form(page_text):
    start_pos = page_text.find('<form class="variations_form cart')
    if start_pos == -1:
        return None
    end_pos = page_text.find(">", start_pos)
    multipart_form = page_text[start_pos:end_pos+1]
    return multipart_form

    
def parse(html_raw):
    tree = html.fromstring(html_raw)
    product = {}
    page_text = html_raw
    product['name'] = tree.xpath('//h1[contains(@class,"product_title")]')[0].text.strip()
    product['categories'] = [tree.xpath('//span[@class="posted_in"]/a')[-1].text]
    
    # out of stock notice
    if tree.xpath('//h6[@class="subscribe_for_interest_text"]'):
        product['prices'] = ["out of stock"]
        return product
        
    product['prices'] = []
    multipart_form = find_multipart_form(page_text)
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
            product['prices'].append(("",price))
        elif len(price_values) == 2:
            price = price_values[0].tail + " - " + price_values[1].tail
            product['prices'].append(("",price))
            
    return product
