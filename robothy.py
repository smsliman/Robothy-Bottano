import musicbrainzngs as mb
import numpy as np
import pandas as pd
import time
import pickle
from sklearn.tree import DecisionTreeClassifier
import math
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pitchfork

mb.set_useragent('robothy bottano', '1.0', 'smsliman@aol.com')
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
with open('robothy_tree_model.pkl', 'rb') as f:
    model = pickle.load(f)

past_reviews = pd.read_csv('fantano_reviews.csv', encoding = "ISO-8859-1")

input = input('Enter an album: ')
done = False
#replace this with more robust levenshtein distance check on names, and additional data for more recent reviews
#Also, lowercasing, and maybe select search result from a list
if input in past_reviews['title'].values:
    old_score = past_reviews.query('title == @input')
    try:
        old_score_string = str(old_score['score']).split('\n')[0].split(' ')[4]
        print('Real Anthony has already reviewed this album. He gave it a: ' + old_score_string)
        done = True
    except Exception:
        #Go back and update once I support not number scores
        print('Real Anthony has already reviewed this album, but did not assign it a number score.')
        done = True

release = mb.search_releases(input)['release-list'][0]

dict = {}

results = sp.search(q=input, limit=1, type='album')
if results is not None:
    if results['albums']['items']:
        id = results['albums']['items'][0]['id']
    else:
        print('TODO')
        #assign neutral values here
    album = sp.album(id)

    artist_id = album['artists'][0]['href']

    artist = sp.artist(artist_id)

    try:
        if (len(input) < 6):
            p = pitchfork.search(artist, input)
        else:
            p = pitchfork.search(artist, input[:5])

        pitchfork_score = p.score();
    except Exception:
        pitchfork_score = 0.0


    if artist['followers']['total']:
        followers = artist['followers']['total']
    else:
        followers = 0

    if artist['genres']:
        genres = artist['genres']
    else:
        genres = ['Unknown']

    if artist['popularity']:
        artist_popularity = artist['popularity']
    else:
        artist_popularity = 0

    if album['popularity']:
        album_popularity = album['popularity']
    else:
        album_popularity = 0

    top_genre = genres[0]

if 'packaging' in release:
    dict['packaging'] = release['packaging']
if 'packaging' not in dict.keys():
    dict['packaging'] = 'None'

if 'artist-credit' in release:
    if release['artist-credit']:
        if 'name' in release['artist-credit'][0]:
            dict['artist-credit-name'] = release['artist-credit'][0]['name']
if 'release-group' in release:
    if 'type' in release['release-group']:
        dict['release-group-type'] = release['release-group']['type']
if 'date' in release:
    dict['date'] = release['date']
if 'date' not in dict.keys():
    dict['date'] = 'Unknown'

if 'country' in release:
    dict['country'] = release['country']
if 'country' not in dict.keys():
    dict['country'] = 'Unknown'

if 'label-info-list' in release:
    if release['label-info-list']:
        if 'label' in release['label-info-list'][0]:
            if 'name' in release['label-info-list'][0]['label']:
                dict['label-info-list-label-name'] = release['label-info-list'][0]['label']['name']
if 'label-info-list-label-name' not in dict.keys():
    dict['label-info-list-label-name'] = 'Unknown'

if 'medium-list' in release:
    if release['medium-list']:
        if 'format' in release['medium-list'][0]:
            dict['medium-list-format'] = release['medium-list'][0]['format']
if 'medium-list-format' not in dict.keys():
    dict['medium-list-format'] = 'CD'
if 'medium-list' in release:
    if release['medium-list']:
        if 'disc-count' in release['medium-list'][0]:
            dict['medium-list-disc-count'] = release['medium-list'][0]['disc-count']
if 'medium-track-count' in release:
    dict['medium-track-count'] = release['medium-track-count']



dict['genres'] = genres
dict['album-popularity'] = album_popularity
dict['artist-popularity'] = artist_popularity
dict['followers'] = followers
dict['top-genre'] = top_genre
dict['pitchfork-score'] = pitchfork_score

# reviews = pd.DataFrame({
# 'packaging': dict['packaging'],
# 'artist-credit-name': dict['artist-credit-name'],
# 'release-group-type': dict['release-group-type'],
# 'date': dict['date'],
# 'country': dict['country'],
# 'label-info-list-label-name': dict['label-info-list-label-name'],
# 'medium-list-format': dict['medium-list-format'],
# 'medium-list-disc-count': dict['medium-list-disc-count'],
# 'medium-track-count': dict['medium-track-count'],
# 'album-popularity': dict['album-popularity'],
# 'artist-popularity': dict['artist-popularity'],
# 'followers': dict['followers'],
# 'top-genre': dict['top-genre']
# }, index=[0])

reviews = pd.DataFrame({
'medium-track-count': dict['medium-track-count'],
'album-popularity': dict['album-popularity'],
'artist-popularity': dict['artist-popularity'],
'followers': dict['followers'],
# 'pitchfork-score': dict['pitchfork-score']
}, index=[0])

reviews.dropna(subset=['medium-track-count'], inplace=True)

values = {
'packaging': 'None',
'date': 'Unknown',
'country': 'Unknown',
'label-info-list-label-name': 'Unknown',
'medium-list-format': 'CD',
'medium-list-disc-count': 0,
'medium-track-count': 0
 }

reviews.fillna(value=values)

data1 = pd.read_csv('data1.csv', encoding = "ISO-8859-1")

data1.append(reviews)
columns = reviews.columns.values
for column in columns:
    text_digit_vals = {}
    def convert_to_int(val):
        return text_digit_vals[val]
    if reviews[column].dtype != np.int64 and reviews[column].dtype != np.float64:
        column_contents = reviews[column].values.tolist()
        unique_elements = set(column_contents)
        x = 0
        for unique in unique_elements:
            if unique not in text_digit_vals:
                text_digit_vals[unique] = x
                x+=1

        reviews[column] = list(map(convert_to_int, reviews[column]))

score = model.predict(reviews)
if done == False:
    print('Robothy Bottano gives this album...')
    print(int(score))
