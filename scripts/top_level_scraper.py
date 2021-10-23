#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


# In[15]:


link = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time"
page = 101
top_100 = []
for x in tqdm(range(1, 26)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    link = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time/{}".format(page)
    page += 100
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['link'] = "https://www.the-numbers.com" + a['href']
            movie['title'] = a.string
            #print("{} : {}".format(title, link))
            top_100.append(movie)
        
len(top_100)


# In[16]:


import pandas as pd
df = pd.DataFrame(top_100)
df


# In[17]:


df[['title','link']].to_csv('/Users/armaan/src/bbox/mdata/thenum/top_level_movies.csv', index=False)

