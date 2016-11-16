# coding=utf-8
# NOTE IMPORTANTI:
# In Collaborative filtering non interessano gli attributi di user e item, interessano solo le interazioni/ratings
# Input principare del CF è User-Rating-Matrix
# In Content Based si devono usare le info (attributi) di users e items
# Input principale del CBF è Item-Content-Matrix

import pandas as pd
import numpy as np
import math

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactionsClean.csv', sep='\t', names=cols)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')
interactions = interactions.drop('create_at', axis=1)

items = pd.read_csv('Dataset/item_profile.csv', sep='\t')
users = pd.read_csv('Dataset/user_profile.csv', sep='\t')
# Sorting the users by user_id
users = users.sort_values(by='user_id')

user_items_dictionary = {}
item_users_dictionary = {}

# Create the dictionaries needed to compute the similarity between users
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
for user, item, interaction in interactions.values:
    user_items_dictionary.setdefault(user, {})[item] = interaction

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    item_users_dictionary.setdefault(item, {})[user] = interaction

# Create the dictionary for the user_user similarity
# dict {user -> (list of {user -> similarity})}
user_user_similarity_dictionary = {}
# For each user in the dictionary
for user in user_items_dictionary:
    # Get the dictionary pointed by the user, containing the items with which the user has interact
    interacted_items = user_items_dictionary.get(user)
    # For each item in the dictionary pointed by the user
    for item in interacted_items:
        # Get the dictionary pointed by the item, containing the users which have interact with the item
        interacted_users = item_users_dictionary.get(item)
        user_list = interacted_users.keys()
        user_user_similarity_dictionary.setdefault(user, {})
        for list_element in user_list:
            if (user_user_similarity_dictionary[user].has_key(list_element)):
                user_user_similarity_dictionary[user][list_element] += 1
            else:
                user_user_similarity_dictionary.setdefault(user, {})[list_element] = 1
    if (user_user_similarity_dictionary[user].has_key(user)):
        del user_user_similarity_dictionary[user][user]


print (user_user_similarity_dictionary)
# # Create the dictionary needed to correctly indexing the matrix
# # count_1 corresponds to the total number of users
# # count_2 corresponds to the total numbers of items
# # dict:u and dict_i correspond to the two dictionaries
# dict_u = {}
# dict_i = {}
# count_1 = 0
# count_2 = 0
# for index,row in users.iterrows():
#     if not dict_u.has_key(row[0]):
#         dict_u[row[0]] = count_1
#         count_1 = count_1 + 1
# for index,row in items.iterrows():
#     if not dict_i.has_key(row[0]):
#         dict_i[row[0]] = count_2
#         count_2 = count_2 + 1
#
# # Inizializing the User Matrix Ratings which contains all the interactions of the users. For now the matrix contains only 0 values
# user_matrix_ratings = np.zeros((count_1,count_2), dtype=np.int32)
# # Populating the User Matrix Ratings. There is no distinction between the interaction_type;
# # all the interactions are treated as 1 (as the prof said to the lesson)
# for index,row in interactions.iterrows():
#     user_matrix_ratings[dict_u[row[0]]][dict_i[row[1]]] = 1
#
# # Inizializing the Similarity matrix of users with all 0 values
# similarity_users = np.zeros((count_1,count_1), dtype=np.int32)
# # Populating the Similarity matrix of users with the formula seen in the lesson.
# # sum corresponds to the numbers of items both users has interacted with
# # u_1 corresponds to the number of items user_1 has interacted with
# # u_2 corresponds to the number of items user_2 has interacted with
# # c1 and c2 are used to iterate over the whole users(remember that count_1 is the number of users)
# for c1 in range(0,count_1):
#     for c2 in range(0,count_1):
#         sum = 0
#         u_1 = 0
#         u_2 = 0
#         if not c1 == c2:
#             for c3 in range(0, count_2):
#                 sum = sum + (user_matrix_ratings[c1][c3]*user_matrix_ratings[c2][c3])
#                 u_1 = u_1 + user_matrix_ratings[c1][c3]
#                 u_2 = u_2 + user_matrix_ratings[c2][c3]
#         if not sum == 0:
#             similarity_users[c1][c2] = sum/(math.sqrt(u_1)*math.sqrt(u_2))
