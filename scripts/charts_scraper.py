#!/usr/bin/env python
# coding: utf-8

# In[188]:


# imports
import requests
import pandas as pd
import urllib
import re
import locale
from bs4 import BeautifulSoup as bs
from time import sleep
pd.set_option('display.float_format', lambda x: '%.2f' % x)
from tqdm import tqdm


# In[189]:


#constants
MOVIE_ATTRIBUTES = {
                    "domestic_box_office", "international_box_office", "worldwide_box_office",
                    "opening_weekend"
                    }

replace_chars = [
    ("\\xc3\\x83\\xc2\\xa9", "é"),
    ("\\xc3\\xa2\\xc2\\x80\\xc2\\xa6", "..."),
    ("\\xc3\\xa2\\xc2\\x80\\xc2\\x9c", "'"),
    ("\\xc3\\xa2\\xc2\\x80\\xc2\\x9d", "'"),
    ("\\n", ""),
    ("\\", ""),
    ("\xc2\\x94", "--"),
    ('â\x80\x99', "'"),
    ("xc3xa2xc2x80xc2x99", "'"),   
    ("xc3xa2xc2x80xc2x94", "—")
    
]

def preprocess_label(label):
    """
    This function will convert label into lower case, combine separate words with an '_' and remove all
    white spaces and other charaters from both the ends.
    """
    
    label = label.lower()
    label = re.sub("[^A-Za-z0-9\s]", "", label)
    label = re.sub("\s{2,}", " ", label)
    label = label.strip()
    label = re.sub("\s", "_", label)
    return label


# In[190]:


def get_movie_details(links, MOVIE_ATTRIBUTES):
    all_movies_info = []
    for link in tqdm(links):
        try:
            r = requests.get(link)
            soup = bs(r.text)
            
            movie = {}

            all_tables = soup.find_all("table")

            
            # Getting title and year 
            main_area = soup.find("div", {"id": "main"})
            name_area = main_area.find("h1")
            name_s = name_area.string
            name_year = name_s.split("(")[-1].strip(')')
            name_x = "(" + name_year + ")"
            name = name_s.replace(name_x, "")
            movie["name"] = name.strip()
            for rc in replace_chars:
                movie["name"] = movie["name"].replace(rc[0], rc[1])
            movie["name"] = movie["name"]

            movie["year"] = name_year
            
            # All box office
            stats_table = all_tables[0]
            stats_table_data = stats_table.findAll("td")
            for index, row in enumerate(stats_table_data):
                data = row.string
                if data:
                    label = preprocess_label(data)
                    if label in MOVIE_ATTRIBUTES:
                        movie[label] = stats_table_data[index+1].string.replace("$","").replace(",","")
            
            all_movies_info.append(movie)
                
        except Exception as ex:
            print(ex, movie, link)
            break
            
    return all_movies_info


# In[191]:


#top 200 domestic
link = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_domestic.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_domestic.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_domestic.csv', index=False)


# In[192]:


#top 200 domestic animated
link = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time-animated"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_domestic.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_domestic.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)

df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_domestic.csv', index=False)


# In[193]:


#top 200 domestic adjusted for inflation
link = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time-inflation-adjusted"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_adjusted_domestic.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_adjusted_domestic.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)

df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_adjusted_domestic.csv', index=False)


# In[194]:


#top 200 international
link = "https://www.the-numbers.com/box-office-records/international/all-movies/cumulative/all-time"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_international.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_international.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)

df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_international.csv', index=False)


# In[195]:


#top 200 international animated
link = "https://www.the-numbers.com/box-office-records/international/all-movies/cumulative/all-time-animated"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_international.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_international.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)

df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_animated_international.csv', index=False)


# In[196]:


#top 200 worldwide
link = "https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/all-time"

top_100 = []
for x in tqdm(range(1, 3)):
    r = requests.get(link)
    soup = bs(r.text, 'html.parser')
    main_table = soup.find("table")
    for a in main_table.find_all('a'):  
        movie = {}
        if 'summary' in a['href']:
            movie['title'] = a.string
            movie['link'] = "https://www.the-numbers.com" + a['href']
            top_100.append(movie)
        
df = pd.DataFrame(top_100)
df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_worldwide.csv', index=False)
top_level_data = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_worldwide.csv')
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES)
df = pd.DataFrame(all_movies)

df.to_csv('/Users/armaan/src/bbox/mdata/thenum/charts/all_time_worldwide.csv', index=False)

