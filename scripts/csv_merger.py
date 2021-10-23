#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import pandas as pd 
from pandas import DataFrame
from slugify import slugify
import requests
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
import webbrowser
pd.set_option('display.float_format', lambda x: '%.2f' % x)
import matplotlib.pyplot as plt
plt.style.use('classic')
import numpy as np
from time import sleep


# In[333]:


#getting both csv files 
movie_details = pd.read_csv('/Users/armaan/src/bbox/mdata/thenum/movie_details.csv') 
imdb_movies = pd.read_csv('/Users/armaan/src/bbox/mdata/imdb/imdb_movies.csv') 
#converting names to lower and some cols to int
movie_details['name_lower'] = movie_details['name'].str.lower()
imdb_movies['year'] = pd.to_numeric(imdb_movies.startYear, errors='coerce')
imdb_movies['primaryTitle_lower'] = imdb_movies['primaryTitle'].str.lower()
imdb_movies['runtimeMinutes'] = pd.to_numeric(imdb_movies.runtimeMinutes, errors='coerce')


# In[334]:


#normalization
def normalize(x):
    if x:
        #for star wars
        x = x.replace('-ep-', '-episode-')
        #for harry potter
        x = x.replace('part-ii', 'part-2')
        x = x.replace('part-i', 'part-1')
        #for e.t. only!
        if x.startswith('et-'):
            x = x.replace('et-', 'e-t-')
        #for rise of skywalker only!
        if x == 'star-wars-the-rise-of-skywalker':
            x = "star-wars-episode-ix-the-rise-of-skywalker"
    return x

#find duplicates
def duplicate_scraper(imdb_id):
    r = requests.get("https://www.imdb.com/title/{}/".format(imdb_id))
    soup = bs(r.text)
    box_office = soup.find("div",{"id": "titleDetails"})
    all_h4 = box_office.findAll("h4")
    drop = True
    for h4 in all_h4:
        if h4.string == "Gross USA:":
            drop = False
            break
    return drop


# In[335]:


#sluggifying and normalizing all names
movie_details['name_slug'] = movie_details.name_lower.apply(slugify)
imdb_movies['name_slug'] = imdb_movies.primaryTitle_lower.apply(slugify)
movie_details['name_slug'] = movie_details.name_slug.apply(normalize)
#creating new df with updated values
new_df = pd.merge(movie_details, imdb_movies, how ='inner', right_on = ['name_slug', 'year'], left_on = ['name_slug', 'year'])


# In[336]:


#find duplicates and get rid of them
duplicates = new_df[new_df.name.duplicated()]
for index, row in tqdm(duplicates.iterrows()):
    match = new_df[(new_df['name'] == row["name"]) & (new_df['year'] == row["year"])]
    if len(match) > 1:
        imdb_ids = match["tconst"]
        for imdb_id in imdb_ids:
            drop = duplicate_scraper(imdb_id)
            if drop == True:
                new_df.drop( new_df[ new_df['tconst'] == imdb_id ].index , inplace=True)


# In[337]:


#drops
new_df = new_df[new_df.tconst != 'tt11861230']
new_df = new_df[new_df.tconst != 'tt4064028']

new_df.drop(["endYear", "isAdult", "titleType", "startYear", "primaryTitle_lower", "runtimeMinutes", "genres", "name_lower", "primaryTitle", "originalTitle"], axis=1, inplace = True)


# In[338]:


#drop movies with missing information
new_df
new_df2 = new_df.dropna(subset=['domestic_box_office', 'international_box_office', 'worldwide_box_office', 'production_budget', 'opening_weekend'])
new_df = new_df2
new_df[:1137]


# In[339]:


#get poster path and add it to new col in df
poster_link_list = []
for p in tqdm(new_df['tconst']):
    tmdb = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US".format(p))
    try:
        poster_path = tmdb.json()['poster_path']
        poster_link = "https://image.tmdb.org/t/p/w300_and_h450_bestv2/{}".format(poster_path)
    except:
        if p:
            print ("no poster for " + p)
    poster_link_list.append(poster_link)

new_df["poster_path"] = poster_link_list


# In[340]:


#get similar movies
def get_matching_similar(df_movies, simlist, how_many=5):
    matching_movies = []
    result_cnt = min(len(simlist), how_many)
    for s in simlist:
        try:
            title = s['title']
            release = int(s['release_date'][:4])
            if len(df_movies[(df_movies.name == title) & (df_movies.year == release)]) == 1:
                poster_path = new_df.loc[new_df['name'] == title, 'poster_path'].values[0]
                name = new_df.loc[new_df['name'] == title, 'name'].values[0]
                movie_link = "{}^{}".format(title, release)
                matching_movies.append({'name': name, 'link': movie_link, 'poster' : poster_path})
                
                if len(matching_movies) >= how_many:
                    break
        except Exception as ex:
            print(ex)

            
    return matching_movies


similar_movies_list = []
x = 0
for t in tqdm(new_df['tconst']):
    turl = "https://api.themoviedb.org/3/movie/{}/similar?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US&page=1".format(t)
    tmdb = requests.get(turl)
    if 'results' in tmdb.json():
        sim_list = tmdb.json()['results']
    else:
        sim_list = []
    similar_movies_list.append(get_matching_similar(new_df, sim_list, how_many=5))
#     x = x+1
#     if x > 3:
#         break
        
new_df["similar_movies"] = similar_movies_list


# In[341]:


#scrape for imdb score
imdb_scores = []
x = 0
for t in tqdm(new_df['tconst']):
    try:
        r = requests.get("https://www.imdb.com/title/{}/".format(t))
        soup = bs(r.text)
        score_section = soup.find("span", {"itemprop": "ratingValue"})
        score = score_section.string
    #     x = x+1
    #     if x > 3:
    #         break
    except Exception as ex:
        score = " "
        print(ex)
        print(t)
    imdb_scores.append(score)
     
new_df["imdb_score"] = imdb_scores


# In[342]:


#get metascore (next use - july26)
# meta_scores = []
# x = 0
# for t in tqdm(new_df['tconst']):
#     url = "http://www.omdbapi.com/?apikey=581c8a90&i={}".format(t)
#     omdb = requests.get(url)
#     info = omdb.json()
#     if info['Metascore']:
#         meta_score = info['Metascore']
#     else:
#         meta_score = "N/A"
#     meta_scores.append(meta_score)
# #     x = x+1
# #     if x > 3:
# #         break


# new_df["meta_score"] = meta_scores


# In[343]:


#make score
bbox_df = new_df2

bbox_df['bb_profit'] = bbox_df.worldwide_box_office - bbox_df.production_budget
bbox_df['bb_profit_multiple'] = bbox_df.worldwide_box_office/bbox_df.worldwide_box_office

bbox_df['bb_profit_score'] = (bbox_df.bb_profit / bbox_df.bb_profit.max()) * 100
bbox_df['bb_profit_multiple_score'] = (bbox_df.bb_profit_multiple / bbox_df.bb_profit_multiple.max()) * 100

bbox_df['bb_score'] = (bbox_df['bb_profit_score']*0.7 + bbox_df['bb_profit_multiple_score']*0.3)


# In[344]:


#find box office shares

bbox_df["domestic_share"] = bbox_df.domestic_box_office / bbox_df.worldwide_box_office * 100
bbox_df["international_share"] = bbox_df.international_box_office / bbox_df.worldwide_box_office * 100
bbox_df.T


# In[345]:


#downloads df to csv
bbox_df = bbox_df[~bbox_df.worldwide_box_office.isnull()]
bbox_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/master_table.csv', index=False)


# In[ ]:




