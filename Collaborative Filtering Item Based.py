import pandas as pd
import math
from collections import OrderedDict

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

target_users = pd.read_csv('Dataset/target_users.csv')

similarity_shrink = 10
prediction_shrink = 0

user_items_dictionary = {}
item_users_dictionary = {}

# Create the dictionaries needed to compute the similarity between users
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, interaction in interactions.values:
    user_items_dictionary.setdefault(user, {})[item] = interaction

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    item_users_dictionary.setdefault(item, {})[user] = interaction

# Create the dictionary for the user_user similarity
# dict {user -> (list of {user -> similarity})}
item_item_similarity_dictionary = {}
print ("Create dictionaries for item-item similarity")
# For each item in the dictionary
for item in item_users_dictionary:
    # Get the dictionary pointed by the item, containing the users which has interact with that item
    interacting_users = item_users_dictionary[item]
    # For each user in the dictionary pointed by the item
    for user in interacting_users:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        interacted_items = user_items_dictionary[user]
        # Get list of items with which this user has interact
        item_list = interacted_items.keys()
        # Instantiate the similarity dictionary
        # dict {item -> (dict2)}
        # dict2 will be {similar_item -> similarity}
        item_item_similarity_dictionary[item] = {}
        # For each item in the list of items
        for list_element in item_list:
            # If similar_item is already in dict2 create the sum of product of ratings
            if (item_item_similarity_dictionary[item].has_key(list_element)):
                item_item_similarity_dictionary[item][list_element] += 1
            # Else the similar_item is added to dict2 and the product of ratings is set to 1
            else:
                item_item_similarity_dictionary[item][list_element] = 1
    # Remove from similar_items the item itself
    if (item_item_similarity_dictionary[item].has_key(item)):
        del item_item_similarity_dictionary[item][item]
    # Evaluate the value of similarity
    for sim in item_item_similarity_dictionary[item]:
        item_item_similarity_dictionary[item][sim] /= ((math.sqrt(len(interacting_users)) *
                                                        math.sqrt(len(item_users_dictionary[sim]))) +
                                                        similarity_shrink)

print ("Create dictionaries for user predictions")
# Create the dictionary for users prediction
# dict {user -> (list of {item -> prediction})}
users_prediction_dictionary = {}
users_prediction_dictionary_num = {}
users_prediction_dictionary_den = {}
# For each target user
for user in target_users['user_id']:
    users_prediction_dictionary_num[user] = {}
    users_prediction_dictionary_den[user] = {}
    # If user has interact with at least one item
    if (user_items_dictionary.has_key(user)):
        # Get dictionary of items with which the user has interact
        i_list = user_items_dictionary[user]
        # For each item in this dictionary
        for item in i_list:
            # Get the dictionary of similar items and the value of similarity
            iis_list = item_item_similarity_dictionary[item]
            # For each similar item in the dictionary
            for item2 in iis_list:
                # If the item was not predicted yet for the user, add it
                if not (users_prediction_dictionary_num[user].has_key(item2)):
                    users_prediction_dictionary_num[user][item2] = iis_list[item2] * 1  # i_list[item]
                    users_prediction_dictionary_den[user][item2] = iis_list[item2]
                # Else Evaluate its contribution
                else:
                    users_prediction_dictionary_num[user][item2] += iis_list[item2] * 1  # i_list[item]
                    users_prediction_dictionary_den[user][item2] += iis_list[item2]

print ("Ratings estimate:")
# For each target user (users_prediction_dictionary_num contains all target users)
for user in users_prediction_dictionary_num:
    users_prediction_dictionary[user] = {}
    # For each item predicted for the user
    for item in users_prediction_dictionary_num[user]:
        # Evaluate the prediction of that item for that user
        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                  (users_prediction_dictionary_den[user][item] + prediction_shrink)

print ("Writing result on CF_Item_Based.csv")
out_file = open("CF_Item_Based.csv","w")
out_file.write('user_id,recommended_items\n')
for user in users_prediction_dictionary:
    if len(users_prediction_dictionary[user].keys()) > 0:
        users_prediction_dictionary[user] = OrderedDict(
            sorted(users_prediction_dictionary[user].items(), key=lambda t: -t[1]))
    x = users_prediction_dictionary[user].keys()
    x = map(str,x)
    out_file.write(str(user) + ',' + ' '.join(x[:min(len(x),5)]) + '\n')

out_file.close()