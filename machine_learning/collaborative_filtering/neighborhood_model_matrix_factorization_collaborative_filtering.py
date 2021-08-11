from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df_ratings = pd.read_csv('./data/ratings.csv')
df_movies = pd.read_csv('./data/movies.csv')

df_user_movie_ratings = df_ratings.pivot(
    index='userId',
    columns='movieId',
    values='rating'
).fillna(0)
df_user_movie_ratings.head()

# matrix는 pivot_table 값을 numpy matrix로 만든 것
matrix = df_user_movie_ratings.to_numpy()

# user_ratings_mean은 사용자의 평균 평점
user_ratings_mean = np.mean(matrix, axis=1)

# R_user_mean : 사용자-영화에 대해 사용자 평균 평점을 뺀 것.
matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)
pd.DataFrame(matrix_user_mean, columns=df_user_movie_ratings.columns).head()

# scipy 에서 제공해주는 svd.
# U 행렬, sigma 행렬, V 전치 행렬을 반환.

U, sigma, Vt = svds(matrix_user_mean, k=12)
print(U.shape)
print(sigma.shape, sigma[0])
print(Vt.shape)

sigma = np.diag(sigma)
print(sigma.shape)
print(sigma[0])
print(sigma[1])

movie_user_rating = user_movie_rating.values.T
movie_user_rating.shape

svd_user_predicted_ratings = np.dot(
    np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
df_svd_preds = pd.DataFrame(
    svd_user_predicted_ratings, columns=df_user_movie_ratings.columns)
df_svd_preds.head()


def recommend_movies(df_svd_preds, user_id, ori_movies_df, ori_ratings_df, num_recommendations=5):
    # 현재는 index로 적용이 되어있으므로 user_id - 1을 해야함
    user_row_number = user_id - 1

    # 최종적으로 만든 pred_df에서 사용자 index에 따라 영화 데이터 정렬 -> 영화 평점이 높은 순으로 정렬됨
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(
        ascending=False)

    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다.
    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    # 위에서 뽑은 user_data와 원본 영화 데이터를 합친다
    user_history = user_data.merge(ori_movies_df, on='movieId').sort_values([
        'rating'], ascending=False)

    # 원본 영화 데이터에서 사용자가 본 영화 데이터를 제외한 데이터를 추출
    recommendations = ori_movies_df[~ori_movies_df['movieId'].isin(
        user_history['movieId'])]

    # 사용자의 영화 평점이 높은 순으로 정렬된 데이터와 위 recommendations를 합친다.
    recommendations = recommendations.merge(pd.DataFrame(
        sorted_user_predictions).reset_index(), on='movieId')

    # 컬럼 이름 바꾸고 정렬해서 반환
    recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values(
        'Predictions', ascending=False).iloc[:num_recommendations, :]

    return user_history, recommendations


already_rated, predictions = recommend_movies(
    df_svd_preds, 330, df_movies, df_ratings, 10)
already_rated.head(10)
predictions
