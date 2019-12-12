import os 

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