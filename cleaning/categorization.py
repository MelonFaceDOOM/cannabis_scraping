import re
import csv


def extract_flower(df):
    # open csv and pull 3 lists from it
    categories = []
    with open("cleaning/categories_flowers.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            categories.append(row)

    categories_with_flower = [category[0] for category in categories if category[1] == 'y']
    df['categories'] = df['categories'].apply(lambda x: [y.strip().lower() for y in x])

    # keep every case with at least one category that is known to contain flower products
    df_flower = df[df['categories'].apply(values_in_reference, reference=categories_with_flower)]

    # further filtering to remove more non-flower products
    df_flower = df_flower[df_flower['prices'].apply(has_weighted_prices)]
    df_flower = df_flower[df_flower['name'].apply(flower_name_filter)]
    df_flower = df_flower[df_flower['prices'].apply(flower_weight_filter)]

    return df_flower


def extract_other(df):
    """Just here to provide a basis to begin looking into other categories in the future"""
    # open csv and pull 3 lists from it
    categories = []
    with open("cleaning/categories_flowers.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            categories.append(row)

    categories_with_flower = [category[0] for category in categories if category[1] == 'y']
    categories_other = [category[0] for category in categories if category[1] == 'n']
    categories_ambiguous = [category[0] for category in categories if category[1] == 'm']

    # separate out categories into new dfs based on 3 lists
    # one product can have multiple categories. If a product has one of the categories that indicates that it is
    # a flower, it should not also be included in "other" or "ambiguous"
    df['categories'] = df['categories'].apply(lambda x: [y.strip().lower() for y in x])
    df_flower = df[df['categories'].apply(values_in_reference, reference=categories_with_flower)]

    df = df.loc[set(df.index) - set(df_flower.index)]
    df_other = df[df['categories'].apply(values_in_reference, reference=categories_other)]
    df = df.loc[set(df.index) - set(df_other.index)]

    return df_other


def values_in_reference(values, reference):
    """Return True if any values are found in a reference list."""
    for v in values:
        if v in reference:
            return True
    return False


def has_weighted_prices(prices):
    """Return True if any price tuple contains two elements.

    Examples:
    prices = [("1g", "$5")("5g","$20")] -- Return True.
    prices = [(, "5")] -- Return False.
    """
    for element in prices:
        if len(element) < 2:
            continue
        if element[0] and element[1]:
            return True
    return False


def flower_name_filter(name):
    """Return False if any non-flower keywords are found in name."""
    name = name.lower()
    not_flower = ['roll', 'hash', 'shatter', 'kief', 'budder', 'trim', 'shake']
    for word in not_flower:
        if word in name:
            return False
    return True
    

def flower_weight_filter(prices):
    """Return False if any keywords are found in the weight variable."""
    rgx_list = ["\dg_\d", "roll", "small", "medium", "large", "sativa", "indica", "lemon", "key", "pink", "mango",
               "strawberry", "sweetsourdick", "gorilla", "blue", "redbull", "love", "watermelon", "dark", "pina",
               "cotton", "honey", "gas", "sour", "tropical", "wellness", "uplift", "alice", "root", "grape", "fruit",
               "pine", "purple", "pot", "5x1g"]
    for element in prices:
        weight = element[0].lower()
        for rgx_pattern in rgx_list:
            if re.search(rgx_pattern, weight):
                return False
    return True
