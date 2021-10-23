#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import pandas as pd 
from pandas import DataFrame
from slugify import slugify
import requests
from tqdm.notebook import tqdm
from time import sleep
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
import webbrowser
pd.set_option('display.float_format', lambda x: '%.2f' % x)
import matplotlib.pyplot as plt
plt.style.use('classic')
import numpy as np


# In[2]:


#get current movies in theatres
tmdb = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US&page=1")
current_results = tmdb.json()['results']
current_movie_titles = [s['title'] for s in current_results]
current_movies_posters = [s['poster_path'] for s in current_results]
current_df = pd.DataFrame()
current_df["title"] = current_movie_titles
current_df["poster_path"] = current_movies_posters
current_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/trending/current_in_theater.csv', index=False)


# In[3]:


#get upcoming movies in theatres
tmdb = requests.get("https://api.themoviedb.org/3/movie/upcoming?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US&page=1")
upcoming_results = tmdb.json()['results']
upcoming_movie_titles = [s['title'] for s in upcoming_results]
upcoming_movies_posters = [s['poster_path'] for s in upcoming_results]
upcoming_df = pd.DataFrame()
upcoming_df["title"] = upcoming_movie_titles
upcoming_df["poster_path"] = upcoming_movies_posters
upcoming_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/trending/upcoming_in_theater.csv', index=False)


# In[4]:


#get popular movies
tmdb = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US&page=1")
popular_results = tmdb.json()['results']
popular_movie_titles = [s['title'] for s in popular_results]
popular_movies_posters = [s['poster_path'] for s in popular_results]
popular_df = pd.DataFrame()
popular_df["title"] = popular_movie_titles
popular_df["poster_path"] = popular_movies_posters
popular_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/trending/popular_movies.csv', index=False)


# In[5]:


#get popular tv shows
tmdb = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=a6837e56522d89b354d01b07e393bebc&language=en-US&page=1")
popular_tv_results = tmdb.json()['results']
popular_tv_titles = [s['name'] for s in popular_tv_results]
popular_tv_posters = [s['poster_path'] for s in popular_tv_results]
popular_df = pd.DataFrame()
popular_df["title"] = popular_tv_titles
popular_df["poster_path"] = popular_tv_posters
popular_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/trending/popular_tv.csv', index=False)

