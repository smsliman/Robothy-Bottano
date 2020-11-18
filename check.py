import numpy as np
import pandas as pd

reviews = pd.read_csv('data.csv')
spotify_data = pd.read_csv('spotify_data.csv')

missing_titles = {}
count = 0
for title in reviews['title'].values:
    if title not in spotify_data['title_'].values:
        missing_titles[count] = title
    count+=1


dupes = reviews.duplicated(subset=['title'])
count_1 = 0
for item in dupes:
    if item:
        print(count_1)
    count_1 +=1
print(dupes)
print(missing_titles)
print(len(reviews['title'].values))
print(len(spotify_data['title_'].values))
