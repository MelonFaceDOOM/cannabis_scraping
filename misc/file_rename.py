import os
from sys import argv
import re
    
inventory_pattern = "[-\w]+_inventory.csv"
scraped_pattern = "[-\w]+_scraped.txt"


# rename all files from "website_inventory.csv" to "inventory"
path = os.path.abspath("sites")
for root, dirs, files in os.walk(path):
    for file in files:
        folder = os.path.split(root)[1]
        folder = os.path.join(os.path.abspath(path), folder)
        original_path = os.path.join(folder, file)
        if re.match(inventory_pattern, file):
            new_path = os.path.join(folder, "inventory.csv")
            os.rename(original_path, new_path)
        elif re.match(scraped_pattern, file):
            new_path = os.path.join(folder, "scraped.txt")
            os.rename(original_path, new_path)
        