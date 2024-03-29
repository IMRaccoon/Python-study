from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

rating_data = pd.read_csv('./data/ratings.csv')
movie_data = pd.read_csv('./data/movies.csv')
movie_data.head()

rating_data.drop('timestamp', axis=1, inplace=True)
rating_data.head()

movie_data.drop('genres', axis=1, inplace=True)
movie_data.head()

user_movie_data = pd.merge(rating_data, movie_data, on='movieId')
user_movie_data.head()

user_movie_rating = user_movie_data.pivot_table(
    'rating', index='userId', columns='title').fillna(0)
user_movie_rating.head()

movie_user_rating = user_movie_rating.values.T
movie_user_rating.shape

SVD = TruncatedSVD(n_components=12)
matrix = SVD.fit_transform(movie_user_rating)
matrix.shape
matrix[0]

corr = np.corrcoef(matrix)
corr.shape

movie_title = user_movie_rating.columns
movie_title_list = list(movie_title)
coffey_hands = movie_title_list.index("Guardians of the Galaxy (2014)")
corr_coffey_hands = corr[coffey_hands]
list(movie_title[(corr_coffey_hands >= 0.9)])[:50]
