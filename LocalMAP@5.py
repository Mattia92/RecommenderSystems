from __future__ import division
import pandas as pd
import CFAlgorithms
import CBAlgorithms
import ValidationAlgorithm as va

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction']
interactions = pd.read_csv('TestDataSet/trainingSet.csv', sep='\t', names=cols, header=0)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

user_cols = ['user', 'job', 'career', 'discipline', 'industry', 'country', 'region', 'experience', 'exp_years', 'exp_years_current',
             'edu_deg', 'edu_fiel']
user_profile = pd.read_csv('DataSet/user_profile.csv', sep='\t', names=user_cols, header=0)

item_cols = ['item', 'title', 'career',	'discipline', 'industry', 'country', 'region', 'latitude', 'longitude',
            'employ', 'tags', 'created_at', 'active_during_test']
item_profile = pd.read_csv('DataSet/item_profile.csv', sep='\t', names=item_cols, header=0)
#item_profile = item_profile.drop(['created_at', 'active_during_test'], 1)

target_users = pd.read_csv('DataSet/target_users.csv')

interacted_users = pd.read_csv('DataSet/interactions.csv', sep='\t', header=0)

validation = pd.read_csv('TestDataSet/validationSet.csv', sep=',', header=0)

#Dictionary of users which has at least one interaction
interacted_users_dictionary = {}
for i, row in interacted_users.iterrows():
    if not (interacted_users_dictionary.has_key(row['user_id'])):
        interacted_users_dictionary[row['user_id']] = 0
for i, row in target_users.iterrows():
    if not (interacted_users_dictionary.has_key(row['user_id'])):
        interacted_users_dictionary[row['user_id']] = 0

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

# Filename for the output result
CB_UB_MAP_Output = "TestDataSet/CB_MAP_User_Based.csv"
CB_IB_MAP_Output = "TestDataSet/CB_MAP_Item_Based.csv"
CF_UB_MAP_Output = "TestDataSet/CF_MAP_User_Based.csv"
CF_IB_MAP_Output = "TestDataSet/CF_MAP_Item_Based.csv"
CF_Hybrid_Weighted_MAP_Output = "TestDataSet/CF_MAP_Hybrid_Weighted.csv"
CF_Hybrid_Ranked_MAP_Output = "TestDataSet/CF_MAP_Hybrid_Ranked.csv"

# Shrink values for Content User Based
CB_UB_similarity_shrink = 10
CB_UB_prediction_shrink = 10

# Shrink values for Collaborative Filtering Item Based
CF_IB_similarity_shrink = 20
CF_IB_prediction_shrink = 10

# Shrink values for Collaborative Filtering User Based
CF_UB_similarity_shrink = 10
CF_UB_prediction_shrink = 10

# Shrink values for Collaborative Filtering Item Based
CF_IB_similarity_shrink = 20
CF_IB_prediction_shrink = 10

# Weight values for Collaborative Filtering, Content Based and Hybrid Ranking
CF_User_Rank_Weight = 0.5
CF_Item_Rank_Weight = 4
CB_User_Rank_Weight = 0.5
CB_Item_Rank_Weight = 0
CF_Hybrid_Rank_Weight = 4

# Weight values for Collaborative Filtering Hybrid Weighted
CF_Hybrid_Weight = 0.4

# Values of KNN for CB Similarities, KNN = 0 means to not use the KNN technique
CB_UB_KNN = 600

# Values of KNN for CF Similarities, KNN = 0 means to not use the KNN technique
CF_UB_KNN = 110
CF_IB_KNN = 0

# Values of KNN for Ranked Prediction
CF_Hybrid_KNN = 30

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}

# Dictionary for using IDF in Collaborative Filtering Item Based
CF_IB_IDF = CFAlgorithms.CF_IDF(interactions)

# Dictionaries for Content User Based Algorithms
# Create the dictionary needed to compute the similarity between users
# It is the User content matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {attribute -> value})}
# Create the dictionary containing for each attribute the list of users which have it
# Dictionary is a list of elements, each element is defined as following
# dict {attribute -> (list of {user -> value})}
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.InitializeDictionaries_user(user_profile, user_cols)

# Dictionaries for Content Item Based Algorithms
#CB_item_attributes_dictionary, CB_attribute_items_dictionary = CBAlgorithms.InitializeDictionaries_item(item_profile, item_cols)

# Compute TF and IDF
print ("Computing TF and IDF")
CB_user_attributes_dictionary, CB_attribute_users_dictionary = CBAlgorithms.ComputeTF_IDF(CB_user_attributes_dictionary, CB_attribute_users_dictionary)
#CB_item_attributes_dictionary, CB_attribute_items_dictionary = CBAlgorithms.ComputeTF_IDF(CB_item_attributes_dictionary, CB_attribute_items_dictionary)
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

# Compute the User-User Similarity for Content User Based
CB_user_user_similarity_dictionary = CBAlgorithms.CBUserUserSimilarity(target_users, CB_user_attributes_dictionary, CB_attribute_users_dictionary,
                                                                       CB_UB_similarity_shrink, CB_UB_KNN)

# Compute the Prediction for Content User Based
CB_UB_users_prediction_dictionary = CBAlgorithms.CBUserBasedPredictRecommendation(target_users, CB_user_user_similarity_dictionary,
                                                                                  CF_user_items_dictionary, active_items_to_recommend,
                                                                                  CB_UB_prediction_shrink)

# Write the final Result for Collaborative Filtering User Based
CBAlgorithms.CBWriteResult(CB_UB_MAP_Output, CB_UB_users_prediction_dictionary)

#CB_item_item_similarity_dictionary = CBAlgorithms.CBItemItemSimilarity(active_items_to_recommend, CB_item_attributes_dictionary,
#                                                                       CB_attribute_items_dictionary, CB_IB_similarity_shrink)

#CB_IB_users_prediction_dictionary = CBAlgorithms.CBItemBasedPredictRecommendation(active_items_to_recommend, CB_item_item_similarity_dictionary,
#                                                                                  CF_user_items_dictionary, target_users_dictionary,
#                                                                                CF_IB_prediction_shrink)

#CBAlgorithms.CBWriteResult(CB_IB_MAP_Output, CB_IB_users_prediction_dictionary)

# Compute the User-User Similarity for Collaborative Filtering User Based
CF_user_user_similarity_dictionary = CFAlgorithms.CFUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                        CF_UB_similarity_shrink, CF_UB_KNN)

# Compute the Prediction for Collaborative Filtering User Based
CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedPredictRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                                   CF_user_items_dictionary, active_items_to_recommend,
                                                                                   CF_UB_prediction_shrink)

# Write the final Result for Collaborative Filtering User Based
# CFAlgorithms.CFWriteResult(CF_UB_MAP_Output, CF_UB_users_prediction_dictionary)

# Compute the Item-Item Similarity for Collaborative Filtering Item Based
CF_item_item_similarity_dictionary = CFAlgorithms.CFItemItemSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                        CF_IB_similarity_shrink, CF_IB_KNN)

# Compute the Prediction for Collaborative Filtering Item Based
CF_IB_users_prediction_dictionary = CFAlgorithms.CFItemBasedPredictRecommendation(target_users, CF_item_item_similarity_dictionary,
                                                                                   CF_user_items_dictionary, active_items_to_recommend,
                                                                                   CF_IB_prediction_shrink, CF_IB_IDF)

# Write the final Result for Collaborative Filtering Item Based
# CFAlgorithms.CFWriteResult(CF_IB_MAP_Output, CF_IB_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Weighted
#CF_HB_Weighted_users_prediction_dictionary = CFAlgorithms.CFHybridWeightedPredictRecommendation(CF_UB_users_prediction_dictionary,
#                                                                                                CF_IB_users_prediction_dictionary,
#                                                                                                CF_Hybrid_Weight)

# Write the final Result for Collaborative Filtering Hybrid Weighted
# CFAlgorithms.CFWriteResult(CF_Hybrid_Weighted_MAP_Output, CF_HB_Weighted_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Rank
CF_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictRecommendation(CF_UB_users_prediction_dictionary,
                                                                                          CF_IB_users_prediction_dictionary,
                                                                                          CF_Hybrid_KNN, CF_User_Rank_Weight,
                                                                                          CF_Item_Rank_Weight)

# Compute the Prediction for Collaborative Filtering and Content Based Hybrid Rank
CF_CB_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictRecommendation(CF_HB_Ranked_users_prediction_dictionary,
                                                                                             CB_UB_users_prediction_dictionary,
                                                                                             CF_Hybrid_KNN, CF_Hybrid_Rank_Weight,
                                                                                             CB_User_Rank_Weight)

# Fill recommendations using Top Popular Algorithm
# CFAlgorithms.Top_Popular_Filling(CF_HB_Ranked_users_prediction_dictionary, CF_IB_IDF)

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_Hybrid_Ranked_MAP_Output, CF_CB_HB_Ranked_users_prediction_dictionary)

# Compute the LocalMAP@5
va.MAP(target_users, validation, CB_UB_MAP_Output)
# va.MAP(target_users, validation, CF_UB_MAP_Output)
# va.MAP(target_users, validation, CF_IB_MAP_Output)
# va.MAP(target_users, validation, CF_Hybrid_Weighted_MAP_Output)
va.MAP(target_users, validation, CF_Hybrid_Ranked_MAP_Output)