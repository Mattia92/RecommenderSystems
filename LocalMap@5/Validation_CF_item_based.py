import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'create_at']
interactions = pd.read_csv('../TestDataSet/trainingSetWithTime.csv', sep='\t', names=cols, header=0)

items = pd.read_csv('../DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]

item_cols = ['item', 'title', 'career',	'discipline', 'industry', 'country', 'region', 'latitude', 'longitude',
            'employ', 'tags', 'created_at', 'active_during_test']
item_profile = pd.read_csv('../DataSet/item_profile.csv', sep='\t', names=item_cols, header=0)

target_users = pd.read_csv('../DataSet/target_users.csv')

# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

# Filename for the output result
CF_IB_predictions_output = "../ValidationPredictions/Validation_CF_Item_Based.csv"

# Shrink values for Collaborative Filtering Item Based
CF_IB_similarity_shrink = 20
CF_IB_prediction_shrink = 10

# Shrink values for Content Item Based
CB_IB_similarity_shrink = 5

# Weight for Hybrid Collaborative Filtering
CF_HB_IB_w = 1.5

# Values of KNN for CF Similarities, KNN = 0 means to not use the KNN technique
CF_IB_KNN = 0

# timestamp of the fifth day before the last interaction
timestamp_last_five_days = 1446508800
timestamp_last_seven_days = 1446336000
timestamp_last_nine_days = 1446163200
timestamp_last_ten_days = 1446076800

# Dictionaries for Collaborative Filtering Algorithms
CF_user_items_dictionary = {}
CF_item_users_dictionary = {}
recent_items_dictionary = {}

# Dictionary for using IDF in Collaborative Filtering Item Based
CF_IB_IDF = CFAlgorithms.CF_IDF(interactions)

# Create the dictionaries needed to compute the similarity between users or items
# It is the User Rating Matrix build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {item -> interaction})}
print ("Create dictionaries for users and items")
for user, item, created in interactions.values:
    CF_user_items_dictionary.setdefault(user, {})[item] = 1 #int(interaction)
    if (created >= timestamp_last_nine_days and not recent_items_dictionary.has_key(item)):
        recent_items_dictionary[item] = 1

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    CF_item_users_dictionary.setdefault(item, {})[user] = 1 #int(interaction)

# Dictionaries for Content Item Based Algorithms
CB_item_attributes_dictionary, CB_attribute_items_dictionary = CBAlgorithms.InitializeDictionaries_item(item_profile, item_cols)

# Compute TF and IDF
print ("Computing TF and IDF")
CB_item_attributes_dictionary, CB_attribute_items_dictionary = CBAlgorithms.ComputeTF_IDF(CB_item_attributes_dictionary, CB_attribute_items_dictionary)

# Compute the Item-Item Similarity for Collaborative Filtering Item Based
CF_item_item_similarity_dictionary = CFAlgorithms.CFHybridItemItemSimilarity(CF_user_items_dictionary, CF_item_users_dictionary,
                                                                                CB_item_attributes_dictionary, CF_IB_similarity_shrink,
                                                                                CB_IB_similarity_shrink, CF_IB_KNN, CF_HB_IB_w)

# Compute the Prediction for Collaborative Filtering Item Based
CF_IB_users_prediction_dictionary = CFAlgorithms.CFItemBasedPredictNormalizedRecommendation(target_users, CF_item_item_similarity_dictionary,
                                                                                            CF_user_items_dictionary, recent_items_dictionary,
                                                                                            active_items_to_recommend, CF_IB_prediction_shrink, CF_IB_IDF)


# Write the final Result for Collaborative Filtering Item Based
CFAlgorithms.CFWrite_Top_Predictions(CF_IB_predictions_output, CF_IB_users_prediction_dictionary)
