from collections import deque
import sqlite3
import requests
from lxml import html

conn = sqlite3.connect('cancrawl.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
             (id integer primary key not null, dt datetime default current_timestamp, url text, html text)''')
conn.commit()

with open("google search/mom_list.txt") as f:
    sites = f.read().splitlines()

for site in sites:
    crawl(base_site = site)

def extract_link(site, a_tag):
    """Extract href attrib from a-tag objects."""
    try:
        href = a_tag.attrib['href']
    except:
        return None
    
    if href.find("#") > -1:
        href = href[:href.find("#")]
        
    if href.find("?") > -1:
        href = href[:href.find("?")]
    
    # if domain isn't included, add it in from the site arg
    if "." not in href:
        href = site.strip("/")+"/"+href.strip("/")
        
    return href

def crawl(base_site):
    queue = deque([base_site])
    visited = []

    #while queue:
    i = 0
    while i < 10:
        i+=1
        url = queue.popleft()
        try:
            page = requests.get(url, timeout=60) # TODO: add headers
        except:
            continue
        tree = html.fromstring(page.content)
        a_tags = tree.xpath('//a')
        for a_tag in a_tags:
            link = extract_link(base_site, a_tag)
            if not link:
                continue
            if (
                link not in queue and
                link not in visited and 
                link.startswith(base_site)
            ):
                queue.append(link)
        visited.append(url)
        c = conn.cursor()
        c.execute("INSERT INTO results(url, html) VALUES (?,?)", [url, page.text])
        conn.commit()
    return None