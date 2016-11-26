import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')
interactions = interactions.drop('create_at', axis=1)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items['item_id']

items = pd.read_csv('DataSet/user_profile.csv', sep='\t', header=0)

target_users = pd.read_csv('DataSet/target_users.csv')

CFOutput = "CF_User_Based.csv"

similarity_shrink = 0
prediction_shrink = 10

# Dictionaries for Content Based Algorithms
CB_user_items_dictionary = {}
CB_item_users_dictionary = {}

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}

# Create the dictionaries needed to compute the similarity between users or items
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, interaction in interactions.values:
    CF_user_items_dictionary.setdefault(user, {})[item] = 1 #int(interaction)

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    CF_item_users_dictionary.setdefault(item, {})[user] = 1 #int(interaction)

CF_user_user_similarity_dictionary = CFAlgorithms.CFUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                    similarity_shrink)
CF_users_prediction_dictionary = CFAlgorithms.CFPredictRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                 CF_user_items_dictionary, prediction_shrink)
CFAlgorithms.CFWriteResult(CFOutput, CF_users_prediction_dictionary)