import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('../DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')
interactions = interactions.drop('create_at', axis=1)

items = pd.read_csv('../DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

target_users = pd.read_csv('../DataSet/target_users.csv')

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

# Filename for the output result
CF_UB_predictions_output = "../Predictions/CF_User_Based.csv"

# Shrink values for Collaborative Filtering User Based
CF_UB_similarity_shrink = 10
CF_UB_prediction_shrink = 10

# Values of KNN for CF Similarities, KNN = 0 means to not use the KNN technique
CF_UB_KNN = 130

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}

# Dictionary for the target users
target_users_dictionary = {}
for user in target_users['user_id']:
    target_users_dictionary[user] = 0

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


# Compute the User-User Similarity for Collaborative Filtering User Based
CF_user_user_similarity_dictionary = CFAlgorithms.CFUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                        CF_UB_similarity_shrink, CF_UB_KNN)

# Compute the Prediction for Collaborative Filtering User Based
CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedPredictNormalizedRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                                            CF_user_items_dictionary, active_items_to_recommend,
                                                                                            CF_UB_prediction_shrink)


# Write the final Result for Collaborative Filtering User Based
CFAlgorithms.CFWritePredictions(CF_UB_predictions_output, CF_UB_users_prediction_dictionary)
