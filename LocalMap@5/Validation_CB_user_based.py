import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction']
interactions = pd.read_csv('../TestDataSet/trainingSetWithTime.csv', sep='\t', names=cols, header=0)

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
CB_UB_predictions_output = "../ValidationPredictions/Validation_CB_User_Based.csv"

# Shrink values for Content User Based
CB_UB_similarity_shrink = 10
CB_UB_prediction_shrink = 10

# Values of KNN for CB Similarities, KNN = 0 means to not use the KNN technique
CB_UB_KNN = 500

timestamp_last_five_day = 1446508800

CF_user_items_dictionary = {}

#DIctionary for number of click on items
item_number_click_dictionary = {}

# Dictionary for the target users
target_users_dictionary = {}
for user in target_users['user_id']:
    target_users_dictionary[user] = 0

# Create the dictionaries needed to compute the similarity between users or items
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, created in interactions.values:
    CF_user_items_dictionary.setdefault(user, {})[item] = 1 #int(interaction)
    if (created >= timestamp_last_five_day):
        if item_number_click_dictionary.has_key(item):
            item_number_click_dictionary[item] += 1
        else:
            item_number_click_dictionary[item] = 1

# return the max number of click on an item in the last 5 days
max_click = 0
for item in item_number_click_dictionary:
    max_click = max(max_click, item_number_click_dictionary[item])

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
                                                                                                       CF_user_items_dictionary, active_items_to_recommend,
                                                                                                       item_number_click_dictionary, max_click, CB_UB_prediction_shrink)

# Write the final Result for Content User Based
CBAlgorithms.CBWrite_Top_Predictions(CB_UB_predictions_output, CB_UB_users_prediction_dictionary_normalized)
