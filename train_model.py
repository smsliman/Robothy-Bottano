import musicbrainzngs as mb
import numpy as np
import pandas as pd
import time
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors, datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.decomposition import PCA
import math
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

import matplotlib.pyplot as plt


mb.set_useragent('robothy bottano', '1.0', 'smsliman@aol.com')
reviews = pd.read_csv('data2.csv', encoding = "ISO-8859-1")

reviews.drop('index', axis=1, inplace=True)
# print(reviews.columns.values)

#in the future, need to instead replace empty scores with values representing appropriate word scores ('not good', 'classic', etc.)
reviews.dropna(subset=['medium-list-disc-count', 'medium-track-count', 'score'], inplace=True)



values = {
'packaging': 'None',
'artist-credit-name': 'Unknown',
'release-group-type': 'Unknown',
'date': 'Unknown',
'country': 'Unknown',
'label-info-list-label-name': 'Unknown',
'medium-list-format': 'CD',
'medium-list-disc-count': 0,
'medium-track-count': 0,
'artist-popularity': 0,
'album-popularity': 0,
'followers': 0,
'top-genre': 'Unknown'
 }

reviews.fillna(value=values)
#do date processing differently, and maybe other values

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


#multisample extreme indexes
extreme_low = reviews[reviews['score']<4.0]
extreme_high = reviews[reviews['score']>8.0]
extremes = [extreme_high*2, extreme_low*2]
reviews = reviews.append(extremes, ignore_index=False)


# feature_cols = [
# 'packaging',
# 'artist-credit-name',
# 'release-group-type',
# 'date',
# 'country',
# 'label-info-list-label-name',
# 'medium-list-format',
# 'medium-list-disc-count',
# 'medium-track-count',
# 'artist-popularity',
# 'album-popularity',
# 'followers',
# 'top-genre',
# 'pitchfork-score'
# ]

#potential reduced list of features
feature_cols = [
'medium-track-count',
'artist-popularity',
'album-popularity',
'followers',
# 'pitchfork-score',
]

counter = 0
X = reviews[feature_cols]

#Tried PCA here i didn't know what I was doing
# pca = PCA(n_components=2)
# pca.fit(reviews)
# print(pca.explained_variance_ratio_)
# print(pca.singular_values_)
# debugger()


y = reviews.score
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=1)

#try different classifiers, maybe some sort of regression, maybe do a train/test split to check accuracy, and perform dimensional regression
#model = DecisionTreeClassifier(criterion='entropy', max_depth=8, min_samples_split=3)
model = RandomForestClassifier()
#model = neighbors.KNeighborsClassifier(n_neighbors = 50, leaf_size = 70)
model = model.fit(X_train,y_train)
y_pred = model.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test,y_pred))
# breakpoint()
# print(model)

with open('robothy_tree_model.pkl', 'wb') as f:
    pickle.dump(model,f)
