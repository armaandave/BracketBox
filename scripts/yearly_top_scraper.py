#!/usr/bin/env python
# coding: utf-8

# In[30]:


#imports
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd
from datetime import date


# In[42]:


year = 1975
current_year = date.today().year

for x in tqdm(range(year, current_year + 1)):
    
    link = "https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{}".format(year)
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.findAll("table")
    main_table = main_table[1]
    yearly_tops = []
    
    for a in main_table.find_all('a'):  
        top_yearly = {}
        if 'summary' in a['href']:
            top_yearly['link'] = "https://www.the-numbers.com" + a['href']
            top_yearly['name'] = a.string
            yearly_tops.append(top_yearly)
        
    df = pd.DataFrame(yearly_tops)
    df.to_csv("/Users/armaan/src/bbox/mdata/thenum/yearly_tops/{}_tops.csv".format(year), index=False)

    year += 1


# In[35]:


year = "2020"
link = "https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{}".format(year)
r = requests.get(link)
soup = bs(r.text, 'html.parser')
main_table = soup.findAll("table")
main_table = main_table[1]

z=0
for x in main_table.findAll("td", {"align": "right"}):
    print (z)
    print (x.string)
    if z > 2:
        print ("---------------------------------")
        z = -1
    z = z + 1

