import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction']
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
CB_IB_predictions_output = "../ValidationPredictions/Validation_CB_Item_Based.csv"

# Shrink values for Content User Based
CB_IB_similarity_shrink = 5
CB_IB_prediction_shrink = 10

# Values of KNN for CB Similarities, KNN = 0 means to not use the KNN technique
CB_IB_KNN = 200
CB_IB_attributes_KNN = 7

# timestamp of the fifth day before the last interaction
timestamp_last_five_days = 1446508800
timestamp_last_seven_days = 1446336000
timestamp_last_ten_days = 1446076800

CF_user_items_dictionary = {}
CF_item_users_dictionary = {}
user_recent_items_dictionary = {}

# Dictionary for using IDF in Collaborative Filtering Item Based
CF_IDF = CFAlgorithms.CF_IDF(interactions)

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
    if created >= timestamp_last_seven_days:
        user_recent_items_dictionary.setdefault(user, {})[item] = 1

# dict {item -> (list of {user -> interaction})}
for user, item, interaction in interactions.values:
    CF_item_users_dictionary.setdefault(item, {})[user] = 1 #int(interaction)

# dict of items which as at least one interaction by target user
item_at_least_one_interaction_by_target_users = {}
for item in CF_item_users_dictionary:
    for user in CF_item_users_dictionary[item]:
        if (target_users_dictionary.has_key(user)):
            item_at_least_one_interaction_by_target_users[item] = 0
            break

# Dictionaries for Content Item Based Algorithms
CB_item_attributes_dictionary, CB_attribute_items_dictionary = CBAlgorithms.InitializeDictionaries_item(item_profile, item_cols)

# Compute TF and IDF
print ("Computing TF and IDF")
CB_item_attributes_dictionary, CB_attribute_items_dictionary, item_interacted_by_target_users_KNN_attributes_dictionary = CBAlgorithms.ComputeTF_IDF_CB_IB(CB_item_attributes_dictionary, CB_attribute_items_dictionary,
                                                                                                active_items_to_recommend, item_at_least_one_interaction_by_target_users,
                                                                                                CB_IB_KNN)

# Compute the Item-Item Similarity for Content Item Based
CB_item_item_similarity_dictionary = CBAlgorithms.CBItemItemSimilarityKNNAttributes(CB_item_attributes_dictionary, CB_attribute_items_dictionary)

CB_item_item_similarity_dictionary = CBAlgorithms.CBItemItemSimilarityEstimateKNNAttributes(CB_item_item_similarity_dictionary, CB_item_attributes_dictionary,
                                                                                            item_interacted_by_target_users_KNN_attributes_dictionary,
                                                                                            CB_IB_similarity_shrink, CB_IB_KNN)

# Compute the Prediction for Content Item Based
CB_IB_users_prediction_dictionary = CBAlgorithms.CBItemKNNAttributesBasedPredictNormalizedRecommendation(active_items_to_recommend, CB_item_item_similarity_dictionary,
                                                                                                         CF_user_items_dictionary, user_recent_items_dictionary,
                                                                                                         target_users_dictionary, CB_IB_prediction_shrink, CF_IDF)

CBAlgorithms.CBWrite_Top_Predictions(CB_IB_predictions_output, CB_IB_users_prediction_dictionary)