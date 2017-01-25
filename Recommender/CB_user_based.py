import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('../DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')

items = pd.read_csv('../DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

user_cols = ['user', 'job', 'career', 'discipline', 'industry', 'country', 'region', 'experience', 'exp_years', 'exp_years_current',
             'edu_deg', 'edu_fiel']
user_profile = pd.read_csv('../DataSet/user_profile.csv', sep='\t',names=user_cols, header=0)

target_users = pd.read_csv('../DataSet/target_users.csv')

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

# Filename for the output result
CB_UB_predictions_output = "../Predictions/CB_User_Based.csv"

# Shrink values for Content User Based
CB_UB_similarity_shrink = 10
CB_UB_prediction_shrink = 10

# Values of KNN for CB Similarities, KNN = 0 means to not use the KNN technique
CB_UB_KNN = 500

# timestamp of the fifth day before the last interaction
timestamp_last_five_days = 1446508800
timestamp_last_seven_days = 1446336000
timestamp_last_ten_days = 1446076800

CF_user_items_dictionary = {}
user_recent_items_dictionary = {}

# Dictionary for the target users
target_users_dictionary = {}
for user in target_users['user_id']:
    target_users_dictionary[user] = 0

# Create the dictionaries needed to compute the similarity between users or items
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, interaction, created in interactions.values:
    CF_user_items_dictionary.setdefault(user, {})[item] = 1 #int(interaction)
    if created >= timestamp_last_seven_days:
        user_recent_items_dictionary.setdefault(user, {})[item] = 1

# Dictionaries for Content User Based Algorithms
# Create the dictionary needed to compute the similarity between users
# It is the User content matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {attribute -> value})}
# Create the dictionary containing for each attribute the list of users which have it
# Dictionary is a list of elements, each element is defined as following
# dict {attribute -> (list of {user -> value})}
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.InitializeDictionaries_user(user_profile, user_cols)

# Compute TF and IDF
print ("Computing TF and IDF")
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.ComputeTF_IDF(CB_user_attributes_dictionary, CB_attribute_users_dictionary)

# Compute the User-User Similarity for Content User Based
CB_user_user_similarity_dictionary = CBAlgorithms.CBUserUserSimilarity(target_users_dictionary, CF_user_items_dictionary, CB_user_attributes_dictionary,
                                                                       CB_attribute_users_dictionary, CB_UB_similarity_shrink, CB_UB_KNN)

CB_UB_users_prediction_dictionary_normalized = CBAlgorithms.CBUserBasedPredictNormalizedRecommendation(target_users_dictionary, CB_user_user_similarity_dictionary,
                                                                                                       CF_user_items_dictionary, user_recent_items_dictionary,
                                                                                                       active_items_to_recommend, CB_UB_prediction_shrink)

# Write the final Result for Content User Based
CBAlgorithms.CBWrite_Top_Predictions(CB_UB_predictions_output, CB_UB_users_prediction_dictionary_normalized)
