#!/usr/bin/env python
# coding: utf-8

# In[53]:


#imports
import pandas as pd 
from tqdm import tqdm
pd.set_option('display.float_format', lambda x: '%.2f' % x)
df = pd.read_csv('/Users/armaan/src/bbox/mdata/final_result/master_table.csv')
df.drop(["bb_profit_multiple_score", "bb_profit_multiple"], axis=1, inplace = True)



# In[54]:

new_df = df
bins = [1980,1985,1990,1995,2000, 2005, 2010, 2015, 2020]
new_df['binned'] = pd.cut(new_df['year'], bins)
year_df = df.groupby('binned').mean()
genre_df = df.groupby('genre').mean()
genre_df
genre_df.drop(["year"], axis=1, inplace = True)
genre_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/genre_table.csv')


# In[55]:


genres = df.genre.unique()
dfs = []
for g in genres:
    dfgenre = df[df.genre == g]
    dfgenre['binned'] = pd.cut(dfgenre['year'], bins)
    dfgmean = dfgenre.groupby('binned').mean()
    dfgmean['genre'] = g
    dfs.append(dfgmean)
len(dfs)


# In[56]:


dfall = pd.concat(dfs)
dfall


# In[57]:


year_df['genre'] = 'All'
year_df


# In[58]:


year_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/binned_table.csv')


# In[59]:


df_final_means = pd.concat([dfall, year_df])
df_final_means.info()


# In[104]:


df = pd.read_csv('/Users/armaan/src/bbox/mdata/final_result/master_table.csv')
ignore_cols = ['year', 'legs', 'bb_profit_multiple', 'bb_profit_multiple_score']
mean_cols = [c for c in df.mean().index if c not in ignore_cols]
mean_df = df.mean()[mean_cols]
median_df = df.median()[mean_cols]
mean_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/final_averages.csv')
median_df.to_csv('/Users/armaan/src/bbox/mdata/final_result/final_medians.csv')


# In[ ]:




