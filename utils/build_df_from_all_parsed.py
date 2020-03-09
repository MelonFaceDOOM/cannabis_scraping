import pandas as pd
import os
import json

def build_df():
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
            df = df.append(df_temp, sort=True)
    df = df.reset_index(drop=True)
    print(f"In total, there are {len(df)} listings")

    return df