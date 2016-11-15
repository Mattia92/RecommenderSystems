import numpy as np
import pandas as pd
import graphlab
# header = ['user_id', 'item_id', 'interaction_type', 'created_at']
# ratings_base = pd.read_csv('DataSet/interactionsClean.csv', sep='\t', names=header)
# n_users = ratings_base.user_id.unique().shape[0]
# n_items = ratings_base.item_id.unique().shape[0]
# print 'Number of users = ' + str(n_users) + ' | Number of jobs = ' + str(n_items)
#
# from sklearn import cross_validation as cv
# train_data, test_data = cv.train_test_split(ratings_base, test_size=0.25)
#
# dict_u = {}
# dict_i = {}
# count_1 = 0
# count_2 = 0
# for line in ratings_base.itertuples():
#     if not dict_u.has_key(line[1]):
#         dict_u[line[1]] = count_1
#         count_1 = count_1 + 1
#     if not dict_i.has_key(line[2]):
#         dict_i[line[2]] = count_2
#         count_2 = count_2 + 1

obs_data = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')

users_info = graphlab.SFrame.read_csv('user_profile_no_null.csv', sep='\t')
users_info['jobroles'] = users_info['jobroles'].apply(lambda x: x.split())

items_info = graphlab.SFrame.read_csv('item_profile_no_null.csv', sep='\t')
items_info['title'] = items_info['title'].apply(lambda x: x.split())
items_info['tags'] = items_info['tags'].apply(lambda x: x.split())

target_users = graphlab.SFrame.read_csv('DataSet/target_users.csv')

item = graphlab.SFrame.read_csv('DataSet/item_profile.csv', sep='\t',)
itemfiltered = item.filter_by(0, 'active_during_test', exclude=True)

itemfilt = itemfiltered.remove_columns(['title', 'career_level', 'discipline_id', 'industry_id', 'country', 'region',
                                        'latitude', 'longitude', 'employment', 'tags', 'created_at', 'active_during_test'])

interactionsToRemove = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')
interactionsToRemove.remove_columns(['interaction_type', 'created_at'])

ran_fact_model = graphlab.recommender.ranking_factorization_recommender.create(observation_data=obs_data, item_id='item_id', user_id='user_id',
                                                                               target='interaction_type', user_data=users_info,
                                                                               item_data=items_info)
recomm = ran_fact_model.recommend(users = target_users, items=itemfilt, k=5, exclude=interactionsToRemove, random_seed=911)

groupedResult = recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('Results/RankingFactorizationMatrix.csv')