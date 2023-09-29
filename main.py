#import streamlit as st
#st.title('.....')

from os import replace
import numpy as np
import pandas as pd
import csv
import ast
import nltk

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')

#genres
#id
#keywords
#title
#overview
#cast
#crew
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

print(movies.isnull().sum())
print(movies.dropna(inplace=True))
print(movies.duplicated().sum())
print(movies.iloc[0].genres)
def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
    return L
movies['genres'] = movies['genres'].apply(convert)


movies['keywords'] = movies['keywords'].apply(convert)

def convert3(obj):
  L=[]
  counter = 0
  for i in ast.literal_eval(obj):
    if counter != 3:
        L.append(i['name'])
        counter+=1
    else:
       break
    return L
movies['cast'] = movies['cast'].apply(convert3)
def fetch_director(obj):
  L = []
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      L.append(i['name'])
      break
  return L
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())

print(movies.head())

def clean_list(lst):
    if lst is not None:
        return [i.replace(" ", "") for i in lst]
    else:
        return []

# Apply the clean_list function to each column
movies['genres'] = movies['genres'].apply(clean_list)
movies['keywords'] = movies['keywords'].apply(clean_list)
movies['cast'] = movies['cast'].apply(clean_list)
movies['crew'] = movies['crew'].apply(clean_list)

print(movies.head())

def clean_list(lst):
    if lst is not None:
        return [i.replace(" ", "") for i in lst]
    else:
        return []

# Apply the clean_list function to each column
movies['genres'] = movies['genres'].apply(clean_list)
movies['keywords'] = movies['keywords'].apply(clean_list)
movies['cast'] = movies['cast'].apply(clean_list)
movies['crew'] = movies['crew'].apply(clean_list)

print(movies.head())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
print(movies.head())
new_df = movies[['movie_id','title','tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
print(new_df.head())
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
  y = []
  for i in text.split():
   y.append(ps.stem(i))
  return " ".join(y)
new_df['tags'] = new_df['tags'].apply(stem)
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
print(new_df.head())
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
print(vectors)
cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movies_list:
    print(new_df.iloc[i[0]].title)
print(recommend('Batman Begins'))
print(new_df.iloc[529].title)
import pickle
pickle.dump(new_df,open('movies.pkl','wb'))

print(new_df['title'].values)
print(pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb')))
print(pickle.dump(similarity,open('similarity.pkl','wb')))