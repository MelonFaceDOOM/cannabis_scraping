import re


def clean_name(text):
    # indica/sativa/hybrid/high cbd are just descriptions, not variants
    # punctuation is removed since it isn't consistent across sites
    # any mention of price is removed
    # AA/AAA/AAAA+ need is removed
    # 'l.s.o.'/'lso' and 'quad' are suppliers, so they are removed from strain names.
        # Careful as it's possible for a future strain name to contain the words 'lso' or 'quad'.

    text = text.lower()
    rgx_list = ['\(.+?\)', '\$.+\/gram', 'a{2,}\+?', '–', '-', '\+ organic farms', '\.', ' by.*$', '^.*:', "'",
               "’", '\*special deal\*', 'indica', 'sativa', 'hybrid', 'bulk', 'quad', 'l\.s\.o\.', 'lso', ' oz',
               "super sale!!", "28g", '(high )?cbd']
    for rgx_pattern in rgx_list:
        text = re.sub(rgx_pattern, '', text)

    # the above step may have left several lingering space characters,
    # so here I replace any sequence of 2 or more spaces with 1 space.
    text = re.sub(' {2,}', ' ', text)
    text = text.strip()
    return text


def specific_replacements(text):
    replacements = {'muffins': 'muffin',
                    'bubble gum': 'bubblegum',
                    'chemdawg': 'chemdog',
                    'cheese #1': 'cheese',
                    'comotose': 'comatose',
                    'vador': 'vader',
                    'zedd': 'zed',
                    'girls': 'girl',
                    'minmosa': 'mimosa',
                    'ó': 'o',
                    'lambs': 'lamb',
                    'chocolate': 'chocolat',
                    'ice wreck': 'icewreck',
                    'original gorilla': 'gorilla',
                    'glue#': 'glue #',
                    'potion #1': 'potion',
                    'potion no 1': 'potion',
                    'grand daddy': 'granddaddy',
                    'king louis xiii': 'king louis',
                    'kush berry': 'kushberry',
                    'sherbert': 'sherbet',
                    'shiskaberry': 'shishkaberry',
                    'train wreck': 'trainwreck',
                    'orange cookies': 'orange cookie',
                    'gsc': 'girl scout cookies',
                    'girlscout': 'girl scout'}

    for k in replacements.keys():
        if k in text:
            text = text.replace(k, replacements[k])
    return text


def standardize_og_kush(text):
    if 'og kush' in text:
        pass
    elif ' og' in text:
        text = text.replace(' og', ' og kush')
    elif ' kush' in text:
        text = text.replace(' kush', ' og kush')
    return text
