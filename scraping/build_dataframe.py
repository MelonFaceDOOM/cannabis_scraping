import os
import pandas as pd
import json


base_dir = "scraping"


def find_sites_with_file(filename, verbose=False):
    """Look at subfolders in base_dir. Return list of subfolder names that contain a specified filename"""
    sites = []
    for root, dirs, files in os.walk(base_dir):
        site = {}
        site['files'] = []
        site['root'] = os.path.basename(root)
        for file in files:
            site['files'].append(file)
        if site['root'] != base_dir:
            sites.append(site)
    sites = list(filter(lambda s: filename in s['files'], sites))
    if verbose:
        print(f"There are {len(sites)} folders with {filename}")
    return sites


def merge_all_parsed(verbose=False):
    """Return dataframe built from all subfolders under base_dir that contain parsed.txt"""
    sites = find_sites_with_file("parsed.txt")
    df = pd.DataFrame(columns=['categories', 'name', 'prices', 'url'])
    for site in sites:
        # assumes site folders are in same parent directory as this file
        file_path = os.path.join(base_dir, site['root'])
        file_path = f"{file_path}/parsed.txt"
        with open(file_path, 'r') as f:
            df_temp = pd.DataFrame(json.load(f))
            df_temp['site'] = site['root']
            df = df.append(df_temp, sort=True)
    df = df.reset_index(drop=True)
    if verbose:
        print(f"In total, there are {len(df)} listings")
    return df


def parse_list(sites):
    # TODO: should sites be an argument, or should it be generated with the find_sites_with_file func?
    """Run parse.py in each subfolder under base_dir that has it"""
    # run parse.py in each folder that has it
    sites = find_sites_with_file("parse.py")
    import subprocess
    for site in sites:
        subprocess.call(["python", "master_parse.py", f"{site['root']}", "-o"])
    return None
