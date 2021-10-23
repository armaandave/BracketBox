#!/usr/bin/env python
# coding: utf-8

# In[75]:


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


# In[76]:


# Constants
URL = "./../mdata/thenum/top_level_movies.csv"
MOVIE_ATTRIBUTES = {
                    "domestic_box_office", "international_box_office", "worldwide_box_office",
                    "opening_weekend", "legs", "production_budget", "theater_counts", "mpaa_rating",
                    "running_time", "franchise", "genre", "production_method", "creative_type",
                    "production_companies"
                    }


# In[77]:


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


# In[78]:


def get_movie_details(links, MOVIE_ATTRIBUTES, verbose=False):
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

            # Opening weekend and budget
            metric_table = all_tables[2]
            metric_table_data = metric_table.findAll("td")
            for index, row in enumerate(metric_table_data):
                data = row.string
                if data:
                    label = preprocess_label(data)
                    if label in {"opening_weekend", "production_budget"}:
                        movie[label] = metric_table_data[index + 1].string.split(" ")[0].replace("$","").replace(",","")

                    if label in {"legs"}:
                        movie[label] = metric_table_data[index + 1].string.split(" ")[0]

                    if label in {"theater_counts"}:
                        pre_count = metric_table_data[index + 1].string.split(", ")[1]
                        movie[label] = pre_count.split(" w")[0]
            
            # Runtime, distributor, mpaa, production method, creative type, production companies, and genre
            details_table = all_tables[5]
            details_table_data = details_table.findAll("td")
            for index, row in enumerate(details_table_data):
                data = row.string
                if data:
                    label = preprocess_label(data)
                    if label in {"running_time"}:
                        movie[label] = details_table_data[index + 1].string.split(" ")[0]
                        
                    if label in {"genre"}:
                        movie[label] = details_table_data[index + 1].string.split(" ")[0]
                    
                    if label in {"creative_type"}:
                        movie[label] = details_table_data[index + 1].string
                        
                    if label in {"production_method"}:
                        movie[label] = details_table_data[index + 1].string
                    
                    if label in {"mpaa_rating"}:
                        movie[label] = details_table_data[index + 1].find("a").string
                    
                    if label in {"production_companies"}:
                        movie[label] = details_table_data[index + 1].find("a").string
            
            # Synopsis
            synopsis_section = soup.find("div", {"id": "summary"})
            synopsis = synopsis_section.find("p")
            if synopsis:
                synopsis_u = str(synopsis.encode(encoding = "UTF-8"))
                synopsis_u = synopsis_u[5:].split("<")[0]
                for rc in replace_chars:
                    synopsis_u = synopsis_u.replace(rc[0], rc[1])
                movie["synopsis"] = synopsis_u
            movie['link'] = link
            all_movies_info.append(movie)
            
            if verbose:
                print(movie)
                
        except Exception as ex:
            print(ex, movie, link)
            break
            
    return all_movies_info


# In[79]:


top_level_data = pd.read_csv(URL)
titles = top_level_data["title"]
links = top_level_data["link"]
all_movies = get_movie_details(links, MOVIE_ATTRIBUTES, False)


# In[80]:


pd.options.display.max_seq_items = 2000
cols_to_num = ['theater_counts', 'opening_weekend', 'domestic_box_office', 'international_box_office',
               'worldwide_box_office', 'production_budget', 'year', 'legs'
              ]
df = pd.DataFrame(all_movies)

#get rid of commas in legs
for x in df["legs"]:
    df["legs"] = x.replace(",", "")

#turn desired cols to numbers
for c in cols_to_num:
    df[c] = pd.to_numeric(df[c])


# In[81]:


df.to_csv('/Users/armaan/src/bbox/mdata/thenum/movie_details.csv', index=False)


# In[ ]:




