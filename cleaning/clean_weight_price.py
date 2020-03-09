import re


def clean_weight(text):
    """Clean weight string through six steps.

    Steps:
    1. Remove parentheses
    2. Remove hyphens
    3. Replace variant string components with standardized ones
    4. Standardize weight unit values
    5. Fix odd numerical values (i.e. 3-5 used instead of 3.5)
    6. Remove extra spaces
    """
    text = text.lower()
    
    # remove anything in parentheses
    text = re.sub('\(.+?\)', '', text)
    # remove hyphen such as 7-grams
    text = re.sub('(\d)\-([A-z])', '\g<1> \g<2>', text)
    
    special_values = {'eighth': '0.125 ounce', 'quarter': '0.25 ounce', 'half': '0.5 ounce', 'half-o': '0.5 ounce',
                      'ounce': '1 ounce','half ounce': '0.5 ounce','quarter-pound': '0.25 pound',
                      'half-pound': '0.5 pound', 'pound': '1 pound', 'gram': '1 g', 'double 28g': '28 g',
                     'half-ounce': '0.5 ounce', 'qp': '0.25 pound', '1': '1 g', '3-5': '3.5 g', '7': '7 g',
                      '14': '14 g', '28': '28 g'}
    try:
        text = special_values[text]
    except:
        pass

    # standardize gram values
    rgx_patterns = ['g *$', 'gr *$', 'gram *$', 'grams *$']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' g', text)
        
    # standardize ounce values
    rgx_patterns = ['oz *$', 'ounce *$', 'ounce-112g-qp', 'ounce-224g-hp']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' ounce', text)
        
    # standardize pound values
    rgx_patterns = ['lb *$', 'pounds *$']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' pound', text)
        
    # standardize some numerical values:
    text = re.sub('3\-5', '3.5', text)
    text = re.sub('0\-5', '0.5', text)
    text = re.sub('0\-25', '0.25', text)
    text = re.sub('(\d)\.0', '\g<1>', text) # 7.0 -> 7
    text = re.sub('1\\\/4', '0.25', text)
    text = re.sub('1\\\/2', '0.5', text)

    # the above steps may have left several lingering space characters,
    # so here I replace any sequence of 2 or more spaces with 1 space.
    text = re.sub(' {2,}', ' ', text)
    text = text.strip()
    
    return text


def split_unit(text):
    """Split string into tuple, returning quantity and weight."""
    units = ['g', 'ounce', 'pound']
    for unit in units:
        if text.find(unit) > -1:
            quantity = float(text[:text.find(unit)])
            break
    else:
        unit = ""
        quantity = text
    return quantity, unit


def convert_to_grams(quantity, unit):
    """Convert ounces and pounds into grams using weedmath."""
    if unit == 'g':
        grams = float(quantity)
    elif unit == 'ounce':
        grams = float(quantity * 28)
    elif unit == 'pound':
        grams = float(quantity * 448)
    else:
        grams = float('nan')
    
    return grams


def clean_dollar_value(text):
    """Standardize dollar strings and convert to float."""
    text = str(text)
    rgx_list = ['\$', '\/', ' ', '[A-z]']
    for rgx_pattern in rgx_list:
        text = re.sub(rgx_pattern, '', text)
    return float(text)


def price_tuple_to_grams(prices):
    """Serialize calling of other cleaning functions so the standard cleaning process can be done with just one func"""
    new_prices = []
    for element in prices:
        price = clean_dollar_value(element[1])
        
        weight = clean_weight(element[0])
        quantity, unit = split_unit(weight)
        grams = convert_to_grams(quantity, unit)
        
        new_prices.append((grams, price))
    return new_prices
