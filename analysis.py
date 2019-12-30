import os 
import json
import pandas as pd
import re
import csv

sites = []
base_dir = "sites"
for root, dirs, files in os.walk(base_dir):
    site = {}
    site['files'] = []
    path = root.split(os.sep)
    site['root'] = os.path.basename(root)
    for file in files:
        site['files'].append(file)
    if site['root'] !=  base_dir:
        sites.append(site)

# keep folders with "scrape.py"
sites = list(filter(lambda s: "scrape.py" in s['files'], sites)) 
# keep folders with "parse.py"
sites_with_parse = list(filter(lambda s: "parse.py" in s['files'], sites)) 

print(f"There are {len(sites)} sites and {len(sites_with_parse)} sites with a parsing script")


# # run parse.py in each folder that has it
# import subprocess
# for site in sites_with_parse:
#     subprocess.call(["python", "master_parse.py", f"sites/{site['root']}", "-o"])


# build dataframe from every "parsed.txt"
sites_with_json = list(filter(lambda s: "parsed.txt" in s['files'], sites)) 

df = pd.DataFrame(columns=['categories', 'name', 'prices', 'url'])
for site in sites_with_json:
    file_path = f"sites/{site['root']}/parsed.txt"
    with open(file_path, 'r') as f:
        df_temp = pd.DataFrame(json.load(f))
        df_temp['site'] = site['root']
        df = df.append(df_temp)
df = df.reset_index(drop=True)


# open csv and pull 3 lists from it
categories = []
with open("categories_flowers.csv", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        categories.append(row)
        
categories_with_flower = [category[0] for category in categories if category[1] == 'y']
categories_other = [category[0] for category in categories if category[1] == 'n']
categories_ambiguous = [category[0] for category in categories if category[1] == 'm']

def values_in_reference(values, reference):
    # make sure case matches for values and reference
    for v in values:
        if v in reference:
            return True
    return False

# separate out categories into new dfs based on 3 lists
# one product can have multiple categories. If a product has one of the categories that indicates that it is
# a flower, it should not also be included in "other" or "ambiguous"
df['categories'] = df['categories'].apply(lambda x: [y.strip().lower() for y in x])
df_flower = df[df['categories'].apply(values_in_reference, reference=categories_with_flower)]
df = df.loc[set(df.index) - set(df_flower.index)]
df_other = df[df['categories'].apply(values_in_reference, reference=categories_other)]
df = df.loc[set(df.index) - set(df_other.index)]
df_ambiguous = df[df['categories'].apply(values_in_reference, reference=categories_ambiguous)]

# identify listings with weighted prices (i.e. this should include flowers and exclude pre-rolls)
def has_weighted_prices(prices):
    for element in prices:
        if len(element) < 2:
            continue
        if element[0] and element[1]:
            return True
    return False

df_weighted_prices = df_flower[df_flower['prices'].apply(has_weighted_prices)]
#df_no_weighted_prices = df_flower.loc[set(df_flower.index) - set(df_weighted_prices.index)]

# remove some more rows based on weights that indicate that they are not flower
def second_flower_filter(prices):
    rgx_list = ["\dg_\d", "roll", "small", "medium", "large", "sativa", "indica"]
    
    for element in prices:
        weight = element[0].lower()
        for rgx_pattern in rgx_list:
            if re.search(rgx_pattern, weight):
                return False
    return True

df_weighted_prices = df_weighted_prices[df_weighted_prices['prices'].apply(second_flower_filter)]

# homogenizing weight values
raw = df_weighted_prices['prices'].map(lambda prices: [price[0] for price in prices]).to_list()
unique_prices = list({price for prices in raw for price in prices })

# cleaning names so it is easier to find identical strains across sites
def clean_weight(text):
    
    text = text.lower()
    
    # remove anything in parentheses
    text = re.sub('\(.+?\)', '', text)
    # remove hyphen such as 7-grams
    text = re.sub('(\d)\-([A-z])', '\g<1> \g<2>', text)
    
    special_values = {'eighth': '0.125 ounce', 'quarter': '0.25 ounce', 'half': '0.5 ounce', 'half-o': '0.5 ounce',
                      'ounce': '1 ounce','half ounce': '0.5 ounce','quarter-pound': '0.25 pound',
                      'half-pound': '0.5 pound', 'pound': '1 pound', 'gram': '1 g'}
    try:
        text = special_values[text]
    except:
        pass

    # standardize gram values
    rgx_patterns = ['g *$', 'gr *$', 'gram *$', 'grams *$']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' g', text)
        
    # standardize ounce values
    rgx_patterns = ['oz *$', 'ounce *$']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' ounce', text)
        
    # standardize pound values
    rgx_patterns = ['lb *$', 'pounds *$']
    for rgx_pattern in rgx_patterns:
        text = re.sub(rgx_pattern, ' pound', text)
        
    # standardize some numerical values:
    text = re.sub('3\-5', '3.5', text)
    text = re.sub('(\d)\.0', '\g<1>', text) # 7.0 -> 7
    text = re.sub('1\\\/4', '0.25', text)
    text = re.sub('1\\\/2', '0.5', text)

    # the above steps may have left several lingering space characters,
    # so here I replace any sequence of 2 or more spaces with 1 space.
    text = re.sub(' {2,}', ' ', text)
    text = text.strip()
    
    return text

def split_unit(text):
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
    text = str(text)
    rgx_list = ['\$', '\/', ' ', '[A-z]']
    for rgx_pattern in rgx_list:
        text = re.sub(rgx_pattern, '', text)
    return float(text)

def price_tuple_to_grams(prices):
    new_prices = []
    for element in prices:
        price = clean_dollar_value(element[1])
        
        weight = clean_weight(element[0])
        quantity, unit = split_unit(weight)
        grams = convert_to_grams(quantity, unit)
        
        new_prices.append((grams, price))
    return new_prices

df_weighted_prices['gram_prices'] = df_weighted_prices['prices'].apply(price_tuple_to_grams)

# # get all values for the 2nd item in the price tuple
# dollar_values = df_weighted_prices['gram_prices'].apply(lambda x: [p[1] for p in x]).to_list()
# # flatten list of lists and keep unique
# dvs = list({item for row in dollar_values for item in row })

#TODO: further cleaning on these cases where the gram value was unable to be cleaned
#TODO: should be as simple as assuming that number = grams, once pre-rolls have been removed (based on name)
def nan_found(prices):
    for price_tuple in prices:
        if price_tuple[0] != price_tuple[0]:
            return True
    return False
    
df_weighted_prices[df_weighted_prices['gram_prices'].apply(nan_found)]

def clean_name(text):
    # indica/sativa/hybrid are just descriptions, not variants
    # punctuation is removed since it isn't consistent across sites
    # any mention of price is removed
    # AAAA is removed
    # 'l.s.o.' and 'quad' are suppliers, so they are removed from strain names.
        # Careful as it's possible for a future strain name to contain the words 'lso' or 'quad'.

    # TODO: "no" <-> "#"
    # TODO: sure there is a space before #
    text = text.lower()
    rgx_list = ['\(.+?\)', '\$.+\/gram', 'a{2,}\+?', '–', '\+ organic farms', '\.', 'by.*$', '^.*:', "'", 
               "’", '\*special deal\*', 'indica', 'sativa', 'hybrid', 'bulk', 'quad', 'l\.s\.o\.']
    for rgx_pattern in rgx_list:
        text = re.sub(rgx_pattern, '', text)

    # the above step may have left several lingering space characters,
    # so here I replace any sequence of 2 or more spaces with 1 space.
    text = re.sub(' {2,}', ' ', text)
    text = text.strip()
    return text

df_weighted_prices['strain'] = df_weighted_prices['name'].apply(clean_name)
# df_weighted_prices['strain'].value_counts().keys().tolist()

def strain_summary(df, strain):
    df = df[df['strain']==strain]
    if len(df) == 0:
        return 'strain not found'
    
    eighth_or_less = []
    quarter_or_less = []
    half_or_less = []
    ounce_or_less = []
    bulk = []
    
    for i, row in df.iterrows():
        for price_tuple in row['gram_prices']:
            if price_tuple[0] <= 3.5:
                eighth_or_less.append(price_tuple)
            elif price_tuple[0] <= 7:
                quarter_or_less.append(price_tuple)
            elif price_tuple[0] <= 14:
                half_or_less.append(price_tuple)
            elif price_tuple[0] <= 28:
                ounce_or_less.append(price_tuple)
            elif price_tuple[0] > 28:
                bulk.append(price_tuple)
                
    def _average(price_tuples):
        prices_per_gram = [p[1]/p[0] for p in price_tuples]
        try:
            price_per_gram = sum(prices_per_gram)/len(prices_per_gram)
        except:
            return float('nan')
        price_per_gram = float("{0:.2f}".format(price_per_gram))
        return price_per_gram
    
    sites = df['site'].tolist()
    print(strain)
    print("found in the following:")
    for site in sites:
        print(f"  - {site}")
    print("\n")
    print("average prices across sites:")
    print(f"3.5g or less: ${_average(eighth_or_less)} per gram" if eighth_or_less else "")
    print(f"3.5-7g:       ${_average(quarter_or_less)} per gram" if quarter_or_less else "")
    print(f"7-14g:        ${_average(half_or_less)} per gram" if half_or_less else "")
    print(f"14-28g:       ${_average(ounce_or_less)} per gram" if ounce_or_less else "")
    print(f"28g+:         ${_average(bulk)} per gram" if bulk else "")
    
    
    
strain_summary(df_weighted_prices, 'gorilla glue #4')

