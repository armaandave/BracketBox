#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np


# In[53]:


class Genre:
    
    @staticmethod
    def get_genres():
        return {
            "Adventure": 100, "Action": 200, "Thriller/Suspense": 300,
            "Musical": 400, "Drama": 500, "Horror": 600
               }


# In[54]:


class ProductionMethod:
    
    @staticmethod
    def get_methods():
        return {
            "Animation/Live Action": 1, "Live Action": 2, "Digital Animation": 3,
            "Hand Animation": 4
               }


# In[55]:


class CreativeType:
    
    @staticmethod
    def get_types():
        return {
            "Science Fiction": 10, "Super Hero": 20, "Historical Fiction": 30,
            "Kids Fiction": 40, "Fantasy": 50, "Dramatization": 60,
            "Contemporary Fiction": 70
               }


# In[56]:


def recommend_similar_movies(df, movie_name, how_many=5):
    
    movie_index = df[df["name"] == movie_name].index[0]
    max_rows = len(df["name"])
    top_index = movie_index - 1
    bottom_index = movie_index + 1
    count = 1
    similar_movies = []
    cur_movie_score = df.iloc[movie_index]["similarity_score"]
    while bottom_index < max_rows and top_index >= 0 and count <= how_many:
        top_score_diff = cur_movie_score - df.iloc[top_index]["similarity_score"]
        bottom_score_diff = df.iloc[bottom_index]["similarity_score"] - cur_movie_score
        if top_score_diff <= bottom_score_diff:
            similar_movies.append(df.iloc[top_index]["name"])
            top_index -= 1
        else:
            similar_movies.append(df.iloc[bottom_index]["name"])
            bottom_index += 1
        count += 1
        
    if count <= how_many:
        while top_index >= 0 and count <= how_many:
            similar_movies.append(df.iloc[top_index]["name"])
            top_index -= 1
            count += 1
        
        while bottom_index < max_rows and count <= how_many:
            similar_movies.append(df.iloc[bottom_index]["name"])
            bottom_index += 1
            count += 1
            
    return similar_movies


# In[ ]:


CSV_FILE = "./../mdata/final_result/master_table.csv"
movies_df = pd.read_csv(CSV_FILE)


# In[57]:


similarity_scores = []
genres = Genre().get_genres()
prod_methods = ProductionMethod().get_methods()
creative_types = CreativeType().get_types()
copy_df = movies_df.copy()
for _, movie in copy_df.iterrows():
    score = genres[movie["genre"]] + prod_methods[movie["production_method"]] +             creative_types[movie["creative_type"]]
    similarity_scores.append(score)
    
copy_df["similarity_score"] = similarity_scores
copy_df.sort_values(by="similarity_score", inplace=True)
copy_df.reset_index(inplace=True)
copy_df.drop("index", axis=1, inplace=True)
copy_df.to_csv("recommendation_df.csv")

