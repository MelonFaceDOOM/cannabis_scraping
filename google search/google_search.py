import re
from googleapiclient.discovery import build
import csv

# list of urls for mail order marijuana websites
with open("mom_list.txt") as f:
    raw = f.read().split('\n')

# standardization: remove preceding scheme/subdomain information 
pattern = "(http:\/\/www\.|https:\/\/www\.|https:\/\/|http:\/\/|www\.|)(.+)\.(ca|com|org|biz|co|net|link|store|shop|ch|green|club)"
mom_urls=[]
for url in raw:
    formatted = ".".join(re.match(pattern, url).groups()[1:3])
    formatted = formatted.lower()
    mom_urls.append(formatted)
mom_urls = list(set(mom_urls))
    
# custom search engine id
with open("gcsekey") as f:
    my_cse_id = f.read()    
# google search api key
with open("gapikey") as f:
    my_api_key = f.read()
    
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res
    
mom_results = []
# it may be necessary to slice mom_urls depending on google search daily limit (100 per day on free plan)
# note that since duplicate urls are dropped via set(), the order will be random
# if you want to process the urls in 100 url chunks,
# you will need to compare the set against already processed urls to avoid repeating 
for url in mom_urls:
    result = google_search('"{url}" -inurl:{url}'.format(url=url), my_api_key, my_cse_id)
    number_of_results = result['queries']['request'][0]['totalResults']
    mom_results.append([url, number_of_results])

#save results to csv
with open('mom_google_results.csv', mode='w') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for result in mom_results:
        w.writerow(result)