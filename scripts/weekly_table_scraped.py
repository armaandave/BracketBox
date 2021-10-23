#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import requests
from bs4 import BeautifulSoup as bs
from tqdm.notebook import tqdm
import pandas as pd
from datetime import date


# In[2]:


link = "https://www.the-numbers.com/weekly-box-office-chart"
r = requests.get(link)
soup = bs(r.text, 'html.parser')
main_table = soup.findAll("table")
main_table = main_table[1]


# In[3]:


top_weekly = []
for a in main_table.find_all('a'):  
    weekly_top = {}
    if 'box-office' in a['href']:
        weekly_top['name'] = a.string
        weekly_top['link'] = "https://www.the-numbers.com" + a['href']
        top_weekly.append(weekly_top)
        df = pd.DataFrame(top_weekly)
        
df


# In[4]:


df[['name','link']].to_csv("/Users/armaan/src/bbox/mdata/thenum/weekly_tops/weekly_tops.csv", index=False)

