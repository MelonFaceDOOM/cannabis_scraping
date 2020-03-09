import argparse
import os
import sys
import json
import csv


def main():
    my_parser = argparse.ArgumentParser(prog="master_parse",
                                        description='parse a scraped mom file')

    my_parser.add_argument('Path',
                           metavar='path',
                           type=str,
                           help='the path to the folder containing the scraped file and the parse file')
                           
    my_parser.add_argument('-f',
                           '--flat',
                           action='store_true',
                           help='save as flat csv file')
                           
    my_parser.add_argument('-o',
                           '--overwrite',
                           action='store_true',
                           help='overwrite existing file without prompt')

    args = my_parser.parse_args()

    # make sure folder exists and that it contains the two necessary files
    folder_path = args.Path
    if not os.path.isdir(folder_path):
        print('The folder path specified does not exist')
        sys.exit()

    scraped_path = os.path.join(folder_path, "scraped.txt")    
    if not os.path.isfile(scraped_path):
        print('The path specified does not contain "scraped.txt"')
        sys.exit()
        
    parse_path = os.path.join(folder_path, "parse.py")
    if not os.path.isfile(parse_path):
        print('The path specified does not contain "parse.py"')
        sys.exit()

    # import parse.py from the folder provided 
    sys.path.append(folder_path)
    from parse import parse

    # open scraped.txt from the folder provided
    with open(scraped_path, 'r') as f:
        page_data = json.load(f)
        
    # remove duplicate urls from page_data
    seen = set()
    page_data = [(url, html) for url, html in page_data
         if not (url in seen or seen.add(url))]

    # use imported parse function for each page
    products=[]
    for page in page_data:
        product = parse(page[1])
        product['url'] = page[0]
        products.append(product)
    
    # flatten if the user passed the -f flag
    if args.flat:
        products_flattened = flatten(products)
        save_path = os.path.join(folder_path, "parsed.csv")
        if not args.overwrite and dont_overwrite(save_path):
            sys.exit()
        with open(save_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator = '\n')
            writer.writerows(products_flattened)
    
    # otherwise save as json in .txt
    else:
        save_path = os.path.join(folder_path, "parsed.txt")
        if not args.overwrite and dont_overwrite(save_path):
            sys.exit()
        with open(save_path, "w") as f:
            json.dump(products, f)
        
    # provide some summary information.
    no_price = [product for product in products if len(product['prices']) == 0]
    one_price = [product for product in products if len(product['prices']) == 1]
    multiple_prices = [product for product in products if len(product['prices']) > 1]
        
    print(f"there were {len(page_data)} urls in source file and {len(products)} products extracted.")
    print(f"{len(no_price)} urls had no price information parsed")
    print(f"{len(one_price)} urls had a single price")
    print(f"{len(multiple_prices)} urls had multiple prices")
    
    
def dont_overwrite(save_path):
    """
    check if a file exists and prompt the user to ask if they would like to overwrite it
    return false if there is no file or if the user answers 'y'
    """
    
    if os.path.isfile(save_path):
        while True:
            overwrite = input(f"{save_path} already exists. Would you like to overwrite? (y/n)\n")
            if overwrite != "y" and overwrite != "n":
                print("please enter 'y' or 'n'")
            else:
                break
    
        if overwrite == "n":
                return True

    return False
    
    
def flatten(products):
    """
    flattens the json object so it can be saved as csv.
    can't just use any pre-built flattening functions because 
    this also splits quantity/price tuple into two columns, 
    and creates a new row for each quantity/price tuple
    """
    
    products_flattened = [["url", "name", "categories", "quantity", "price"]]
    for product in products:
        # concat instances of multiple categories
        if product['categories']:
            categories = ", ".join(product['categories']) 
        else:
            categories = None
        
        prices = product['prices']
        if prices:
            # create a new row for each qty/price tuple.
            for price in prices:
                products_flattened.append([product['url'], product['name'], categories, 
                                           price[0], price[1]])
        else:
            products_flattened.append([product['url'], product['name'], categories, ""])
    return products_flattened


if __name__ == "__main__":
    main()