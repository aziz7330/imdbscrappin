# importing required Libraries
import pandas as pd  # to create dataframe
import requests  # to send the request to the URL
from bs4 import BeautifulSoup  # to get the content in the form of HTML
import csv
import numpy as np  # to count the values (in our case)
# assigning the URL with variable name url
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
# request allow you to send HTTP request
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# creating an empty list, so that we can append the values
movie_name = []
year = []
time = []
rating = []
genres = []
metascore = []
votes = []


movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
for store in movie_data:
    name = store.h3.a.text
    movie_name.append(name)
    year_of_release = store.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
    year.append(year_of_release)
    runtime = store.p.find('span', class_='runtime').text.replace(' min','')
    time.append(runtime)
    rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','')
    rating.append(rate)
    genre = store.find('span', class_='genre').text.replace('\n', '')
    genres.append(genre)
    meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else 'Nan'
    metascore.append(meta)
    value = store.find_all('span', attrs={'name': 'nv'})
    vote = value[0].text
    votes.append(vote)
movie_DF = pd.DataFrame(
    {'Name of movie': movie_name, 'Year of relase': year, 'genre': genres, 'Watchtime': time, 'Movie Rating': rating,
     'Metascore': metascore, 'Votes': votes})
movie_DF.to_csv('moviedata.csv')
