import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'create_at']
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
CF_UB_predictions_output = "../ValidationPredictions/Validation_CF_User_Based.csv"

# Shrink values for Collaborative Filtering User Based
CF_UB_similarity_shrink = 10
CF_UB_prediction_shrink = 10

# Shrink values for Content User Based
CB_UB_similarity_shrink = 10

# Weight for Hybrid Collaborative Filtering
CF_HB_UB_w = 1.1

# Values of KNN for CF Similarities, KNN = 0 means to not use the KNN technique
CF_UB_KNN = 130

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}
CF_user_items_dictionary_time = {}

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
    if(interaction >= 1446336000):
        CF_user_items_dictionary_time.setdefault(user, {})[item] = 1


# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    CF_item_users_dictionary.setdefault(item, {})[user] = 1 #int(interaction)

# Dictionaries for Content User Based Algorithms
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.InitializeDictionaries_user(user_profile, user_cols)

# Compute TF and IDF
print ("Computing TF and IDF")
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.ComputeTF_IDF(CB_user_attributes_dictionary, CB_attribute_users_dictionary)

# Compute the User-User Similarity for Collaborative Filtering User Based
CF_user_user_similarity_dictionary = CFAlgorithms.CFHybridUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                                CB_user_attributes_dictionary, CF_UB_similarity_shrink,
                                                                                CB_UB_similarity_shrink, CF_UB_KNN, CF_HB_UB_w)

# Compute the Prediction for Collaborative Filtering User Based
CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedPredictNormalizedRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                                            CF_user_items_dictionary, active_items_to_recommend,
                                                                                            CF_UB_prediction_shrink)

#CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedLastWeekPredictNormalizedRecommendation(target_users, CF_user_user_similarity_dictionary,
#                                                                                                    CF_user_items_dictionary, CF_user_items_dictionary_time,
#                                                                                                    active_items_to_recommend, CF_UB_prediction_shrink)

# Write the final Result for Collaborative Filtering User Based
CFAlgorithms.CFWrite_Top_Predictions(CF_UB_predictions_output, CF_UB_users_prediction_dictionary)