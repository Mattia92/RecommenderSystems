# coding=utf-8
# NOTE IMPORTANTI:
# In Collaborative filtering non interessano gli attributi di user e item, interessano solo le interazioni/ratings
# Input principare del CF è User-Rating-Matrix
# In Content Based si devono usare le info (attributi) di users e items
# Input principale del CBF è Item-Content-Matrix

import pandas as pd
import numpy as np
import math
import pickle as p
from collections import OrderedDict
from operator import itemgetter

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactions.csv', sep='\t', names=cols)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')
interactions = interactions.drop('create_at', axis=1)

items = pd.read_csv('Dataset/item_profile.csv', sep='\t')
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items['item_id']

users = pd.read_csv('Dataset/user_profile.csv', sep='\t')
target_users = pd.read_csv('Dataset/target_users.csv')

# Sorting the users by user_id
users = users.sort_values(by='user_id')

shrink = 10

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
        # Get list of users which have interacted with the same item of the first user
        user_list = interacted_users.keys()
        # Instantiate the similarity dictionary
        # dict {user -> (dict2)}
        # dict2 will be {similar_user -> similarity}
        user_user_similarity_dictionary.setdefault(user, {})
        for list_element in user_list:
            # If similar_user is already in dict2 create the sum of product of ratings
            if (user_user_similarity_dictionary[user].has_key(list_element)):
                user_user_similarity_dictionary[user][list_element] += 1
            # Else the product of ratings is set to 1
            else:
                user_user_similarity_dictionary.setdefault(user, {})[list_element] = 1
    # Remove from similar_users the user itself
    if (user_user_similarity_dictionary[user].has_key(user)):
        del user_user_similarity_dictionary[user][user]
    # Calculate the value of similarity
    for sim in user_user_similarity_dictionary[user]:
        user_user_similarity_dictionary[user][sim] /= (math.sqrt(len(interacted_items))*math.sqrt(len(user_items_dictionary.get(sim))))

#TODO: ordinare dizionario in base al valore delle similarity
#TODO: considerare solo KNN most similar users

# Create the dictionary for users prediction
# dict {user -> (list of {item -> prediction})}
users_prediction_dictionary = {}
users_prediction_dictionary_num = {}
users_prediction_dictionary_den = {}
# For each target user
for user in target_users['user_id']:
    print (user)
    users_prediction_dictionary_num[user] = {}
    users_prediction_dictionary_den[user] = {}
    # If user has similar users
    if (user_user_similarity_dictionary.has_key(user)):
        # Get list of similar users
        uus_list = user_user_similarity_dictionary[user]
        # For each similar user
        for user2 in uus_list:
            u2_item_list = user_items_dictionary[user2]
            for i in u2_item_list:
                if not (users_prediction_dictionary_num[user].has_key(i)):
                    users_prediction_dictionary_num[user][i] = uus_list[user2] * u2_item_list[i]
                    users_prediction_dictionary_den[user][i] = uus_list[user2]
                else:
                    users_prediction_dictionary_num[user][i] += uus_list[user2] * u2_item_list[i]
                    users_prediction_dictionary_den[user][i] += uus_list[user2]

for user in users_prediction_dictionary_num:
    users_prediction_dictionary[user] = {}
    for item in users_prediction_dictionary_num[user]:
        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                  (users_prediction_dictionary_den[user][item] + shrink)


p.dump(users_prediction_dictionary, open("prediction.p", "wb"))
user_prediction = p.load( open( "prediction.p", "rb" ) )