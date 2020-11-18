import musicbrainzngs as mb
import numpy as np
import pandas as pd
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

mb.set_useragent('robothy bottano', '1.0', 'smsliman@aol.com')
reviews = pd.read_csv('data.csv')

reviews = reviews.drop_duplicates(subset=['title'])
print(reviews)
breakpoint()

genre_dict = {}
album_popularity_dict = {}
artist_popularity_dict = {}
followers_dict = {}
top_genre_dict = {}
title_dict = {}
count = 0
check = 0
previous_title = ' '
for title in reviews['title'].values:
    print(count)
    print(len(genre_dict))
    past_check = check
    check = count-len(genre_dict)
    if past_check-check != 0:
        print('Previous Title:')
        print(previous_title)

        title_dict[previous_title] = previous_title
        genre_dict[previous_title] = ['Unknown']
        album_popularity_dict[previous_title] = 0
        artist_popularity_dict[previous_title] = 0
        followers_dict[previous_title] = 0
        top_genre_dict[previous_title] = 'Unknown'
        print(title_dict[previous_title])
    previous_title = title

    results = sp.search(q=title, limit=1, type='album')
    # print(len(reviews['title'].values))
    # print(results)
    # breakpoint()
    if results:
        if results['albums']['items']:
            id = results['albums']['items'][0]['id']
        else:
            title_dict[title] = title
            genre_dict[title] = ['Unknown']
            album_popularity_dict[title] = 0
            artist_popularity_dict[title] = 0
            followers_dict[title] = 0
            top_genre_dict[title] = 'Unknown'
            count +=1
            print('Title:')
            print(title)
            continue
        album = sp.album(id)

        artist_id = album['artists'][0]['href']

        artist = sp.artist(artist_id)

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


        top_genre_dict[title] = top_genre
        followers_dict[title] = followers
        genre_dict[title] = genres
        album_popularity_dict[title] = album_popularity
        artist_popularity_dict[title] = artist_popularity
        title_dict[title] = title
    else:
        print('skip')
        genre_dict[title] = ['Unknown']
        album_popularity_dict[title] = 0
        artist_popularity_dict[title] = 0
        followers_dict[title] = 0
        top_genre_dict[title] = 'Unknown'

    count +=1

genre_series = pd.Series(genre_dict)
album_popularity_series = pd.Series(album_popularity_dict)
artist_popularity_series = pd.Series(artist_popularity_dict)
followers_series = pd.Series(followers_dict)
top_genre_series = pd.Series(top_genre_dict)
title_series = pd.Series(title_dict)

spotify_data = pd.DataFrame({
'title_': title_dict,
'genres': genre_series,
'album-popularity': album_popularity_series,
'artist-popularity': artist_popularity_series,
'followers': followers_series,
'top-genre': top_genre_series
})

final_frame = pd.concat([reviews, spotify_data], sort=False, axis=1)
breakpoint()

try:
    final_frame.to_csv('data1.csv', index=False)
    spotify_data.to_csv('spotify_data.csv', index=False)
except Exception:
    print('error writing to file')
    breakpoint()
