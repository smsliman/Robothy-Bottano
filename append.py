import numpy as np
import pandas as pd

reviews = pd.read_csv('data1.csv')
pitchfork_data = pd.read_csv('pitchfork_data.csv')

reviews = reviews.drop_duplicates(subset=['title'], ignore_index=True)

reviews['pitchfork-score'] = pitchfork_data
breakpoint()

reviews.to_csv('data2.csv', index=False)
