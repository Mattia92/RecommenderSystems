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
items = graphlab.SFrame.read_csv('item_profile_no_null.csv', sep='\t')

items['title'] = items['title'].apply(lambda x: x.split())
items['tags'] = items['tags'].apply(lambda x: x.split())

print items