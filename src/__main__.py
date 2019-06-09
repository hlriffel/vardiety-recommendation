from turicreate import item_similarity_recommender, SFrame

import pandas as pd
# import numpy as np

data_path = '/home/riffel/Projects/vardiety/vardiety-recommendation/data'

combinations = pd.read_csv(data_path + '/combinations.csv', sep=',', names=['combination_id', 'items'])
preferences = pd.read_csv(data_path + '/preferences.csv', sep=',', names=['user_id', 'combination_id', 'rating'])

ratings = pd.merge(combinations, preferences, on='combination_id')

ratings_frame = SFrame(ratings)

print(ratings_frame)

item_sim_model = item_similarity_recommender.create(
    ratings_frame,
    user_id='user_id',
    item_id='combination_id',
    target='rating',
    similarity_type='pearson'
)

item_sim_recom = item_sim_model.recommend(users=[2], k=10)

print(item_sim_recom)

'''
n_users = ratings.user_id.unique().shape[0]
n_combinations = ratings.combination_id.unique().shape[0]

data_matrix = np.zeros((n_users, n_combinations))

for line in ratings.itertuples():
    data_matrix[line[3] - 1, line[1] -1] = line[4]

user_similarity = pairwise_distances(data_matrix, metric='cosine')
item_similarity = pairwise_distances(data_matrix.T, metric='cosine')


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_ratings = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_ratings[:, np.newaxis])
        pred = mean_user_ratings[:, np.newaxis] + \
               similarity.dot(ratings_diff) /\
               np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])

    return pred


user_prediction = predict(data_matrix, user_similarity, type='user')
item_prediction = predict(data_matrix, item_similarity, type='item')

print(data_matrix)
print('-----------------')
print(user_prediction)
print(item_prediction)

'''
