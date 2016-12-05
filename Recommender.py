import pandas as pd
import CFAlgorithms
import CBAlgorithms
import math
import numpy

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by='create_at')
interactions = interactions.drop('create_at', axis=1)

user_cols = ['user', 'job', 'career', 'discipline', 'industry', 'country', 'region', 'experience', 'exp_years', 'exp_years_current',
                   'edu_deg', 'edu_fiel']
user_profile = pd.read_csv('DataSet/user_profile.csv', sep='\t',names=user_cols, header=0)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

target_users = pd.read_csv('DataSet/target_users.csv')

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

CF_UB_Output = "Results/CF_User_Based.csv"
CF_IB_Output = "Results/CF_Item_Based.csv"
CF_Hybrid_Weighted_Output = "Results/CF_Hybrid_Weighted.csv"
CF_Hybrid_Ranked_Output = "Results/CF_Hybrid_Ranked.csv"

# Shrink values for Collaborative Filtering User Based
CF_UB_similarity_shrink = 10
CF_UB_prediction_shrink = 10

# Shrink values for Collaborative Filtering Item Based
CF_IB_similarity_shrink = 20
CF_IB_prediction_shrink = 10

# Weight values for Collaborative Filtering Hybrid Ranking
CF_User_Rank_Weight = 0.5
CF_Item_Rank_Weight = 4

# Weight values for Collaborative Filtering Hybrid Weighted
CF_Hybrid_Weight = 0.4

# Values of KNN for CF Similarities, KNN = 0 means to not use the KNN technique
CF_UB_KNN = 110
CF_IB_KNN = 0

# Values of KNN for Ranked Prediction
CF_Hybrid_KNN = 30

# Dictionaries for Content Based Algorithms
CB_user_items_dictionary = {}
CB_item_users_dictionary = {}

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}

# Dictionary for using IDF in Collaborative Filtering Item Based
CF_IB_IDF = {}

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

print ("Create dictionary for CF_IDF")
for user, item, interaction in interactions.values:
    CF_IB_IDF[item] = 0
for user, item, interaction in interactions.values:
    CF_IB_IDF[item] += 1

print("Create dictionaries for content based algorithm")
# Create the dictionary needed to compute the similarity between users
# It is the User content matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {attribute -> 1})}
users_attributes = {}
#for each row of the user_profile csv
for i, row in user_profile.iterrows():
    #initialize the dictionary of the user
    users_attributes[row['user']] = {}
    #for each attribute of the user
    for att in user_cols:
        if not(att == 'user'):
             #if the attribute is jobroles then split the string obtaining the various jobs and insert them in the dictionary
             #if the value of the field jobroles is 0 insert nothing
             if (att == 'job'):
                 if not(row[att] == '0'):
                    jobs = str(row[att]).split(",")
                    for j in jobs:
                        users_attributes[row['user']][att + '_' + str(j)] = 1
             # if the attribute is edu_fieldofstudies then split the string obtaining the various fields and insert them in
             # the dictionary
             elif(att == 'edu_fiel'):
                 if type(row[att]) == str:
                     fields = str(row[att]).split(",")
                     for f in fields:
                         users_attributes[row['user']][att + '_' + str(f)] = 1
             # if the attribute is country dont't consider float values
             elif(att == 'country'):
                 if type(row[att]) == str:
                     users_attributes[row['user']][att + '_' + str(row[att])] = 1
             #if the column type is int or float discard Null values
             elif(user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                 if not(math.isnan(row[att])):
                     users_attributes[row['user']][att + '_' + str(row[att])] = 1
             else:
                 users_attributes[row['user']][att + '_' + str(row[att])] = 1

# Create the dictionary containing for each attribute the list of users which have it
# Dictionary is a list of elements, each element is defined as following
# dict {attribute -> (list of {user -> 1})}
attributes_users = {}
#for each row of the user_profile csv
for i, row in user_profile.iterrows():
    #for each attribute of the user
    for att in user_cols:
        if not(att == 'user'):
             #if the attribute is jobroles then split the string obtaining the various jobs and insert them in the dictionary
             #if the value of the field jobroles is 0 insert nothing
             if (att == 'job'):
                 if not(row[att] == '0'):
                    jobs = str(row[att]).split(",")
                    for j in jobs:
                        # if the dictionary is not already inizialized do it
                        if not attributes_users.has_key(att + '_' + str(j)):
                            attributes_users[att + '_' + str(j)] = {}
                        attributes_users[att + '_' + str(j)][row['user']] = 1
             # if the attribute is edu_fieldofstudies then split the string obtaining the various fields and insert them in
             # the dictionary
             elif(att == 'edu_fiel'):
                 if type(row[att]) == str:
                     fields = str(row[att]).split(",")
                     for f in fields:
                         if not attributes_users.has_key(att + '_' + str(f)):
                             attributes_users[att + '_' + str(f)] = {}
                         attributes_users[att + '_' + str(f)][row['user']] = 1
             # if the attribute is country dont't consider float values
             elif(att == 'country'):
                 if type(row[att]) == str:
                     if not attributes_users.has_key(att + '_' + str(row[att])):
                         attributes_users[att + '_' + str(row[att])] = {}
                     attributes_users[att + '_' + str(row[att])][row['user']] = 1
             #if the column type is int or float discard Null values
             elif(user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                 if not(math.isnan(row[att])):
                     if not attributes_users.has_key(att + '_' + str(row[att])):
                         attributes_users[att + '_' + str(row[att])] = {}
                     attributes_users[att + '_' + str(row[att])][row['user']] = 1
             else:
                 if not attributes_users.has_key(att + '_' + str(row[att])):
                     attributes_users[att + '_' + str(row[att])] = {}
                 attributes_users[att + '_' + str(row[att])][row['user']] = 1

# Compute the User-User Similarity for Collaborative Filtering User Based
CF_user_user_similarity_dictionary = CFAlgorithms.CFUserUserSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                       CF_UB_similarity_shrink, CF_UB_KNN)
# Compute the Prediction for Collaborative Filtering User Based
CF_UB_users_prediction_dictionary = CFAlgorithms.CFUserBasedPredictRecommendation(target_users, CF_user_user_similarity_dictionary,
                                                                                  CF_user_items_dictionary, active_items_to_recommend,
                                                                                  CF_UB_prediction_shrink)

# Write the final Result for Collaborative Filtering User Based
CFAlgorithms.CFWriteResult(CF_UB_Output, CF_UB_users_prediction_dictionary)

# Compute the Item-Item Similarity for Collaborative Filtering Item Based
CF_item_item_similarity_dictionary = CFAlgorithms.CFItemItemSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                       CF_IB_similarity_shrink, CF_IB_KNN)

# Compute the Prediction for Collaborative Filtering Item Based
CF_IB_users_prediction_dictionary = CFAlgorithms.CFItemBasedPredictRecommendation(target_users, CF_item_item_similarity_dictionary,
                                                                                  CF_user_items_dictionary, active_items_to_recommend,
                                                                                  CF_IB_prediction_shrink, CF_IB_IDF)
# Write the final Result for Collaborative Filtering Item Based
CFAlgorithms.CFWriteResult(CF_IB_Output, CF_IB_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Weighted
CF_HB_Weighted_users_prediction_dictionary = CFAlgorithms.CFHybridWeightedPredictRecommendation(CF_UB_users_prediction_dictionary,
                                                                               CF_IB_users_prediction_dictionary, CF_Hybrid_Weight)

# Write the final Result for Collaborative Filtering Hybrid Weighted
CFAlgorithms.CFWriteResult(CF_Hybrid_Weighted_Output, CF_HB_Weighted_users_prediction_dictionary)

# Compute the Prediction for Collaborative Filtering Hybrid Rank
CF_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictRecommendation(CF_UB_users_prediction_dictionary,
                                                                                     CF_IB_users_prediction_dictionary, CF_Hybrid_KNN,
                                                                                     CF_User_Rank_Weight, CF_Item_Rank_Weight)

# Fill recommendations using Top Popular Algorithm
CFAlgorithms.Top_Popular_Filling(CF_HB_Ranked_users_prediction_dictionary, CF_IB_IDF)

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_Hybrid_Ranked_Output, CF_HB_Ranked_users_prediction_dictionary)