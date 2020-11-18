import numpy as np
import pandas as pd

reviews = pd.read_csv('data2.csv')
spotify_data = pd.read_csv('spotify_data.csv')

reviews = reviews.drop_duplicates(subset=['title'], ignore_index=True)
print(len(reviews['country'].values))

final_frame = pd.concat([reviews, spotify_data], sort=False, axis=1)
breakpoint()

final_frame.to_csv('data2.csv', index=False)
