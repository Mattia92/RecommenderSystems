import CBAlgorithms
import CFAlgorithms
import MLAlgorithms
import pandas as pd
import ValidationAlgorithm as va

target_users = pd.read_csv('../DataSet/target_users.csv')
validation = pd.read_csv('../TestDataSet/validationSet.csv', sep=',', header=0)

cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('../DataSet/interactions.csv', sep='\t', names=cols, header=0)

# Filename for the output result
CB_UB_predictions_output = "../ValidationPredictions/Validation_CB_User_Based.csv"
CB_IB_predictions_output = "../ValidationPredictions/Validation_CB_Item_Based.csv"
CF_UB_predictions_output = "../ValidationPredictions/Validation_CF_User_Based.csv"
CF_IB_predictions_output = "../ValidationPredictions/Validation_CF_Item_Based.csv"
ML_SVD_predictions_output = "../ValidationPredictions/Validation_Funk_SVD_2.csv"

# Filename for the output result
CB_UB_MAP_Output = "../TestDataSet/CB_MAP_User_Based.csv"
CB_IB_MAP_Output = "../TestDataSet/CB_MAP_Item_Based.csv"
CF_HB_UB_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_User_Based.csv"
CF_HB_IB_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_Item_Based.csv"
ML_SVD_MAP_Output = "../TestDataSet/CF_MAP_FunkSVD.csv"
CF_Hybrid_Ranked_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_Ranked.csv"
ML_Funk_SVD_MAP_Output = "../TestDataSet/CF_MAP_FunkSVD.csv"
CF_CB_ML_Hybrid_MAP_Output = "../TestDataSet/CF_CB_ML_MAP_Hybrid_Ranked.csv"

# Weight values for Collaborative Filtering, Content Based and Hybrid Ranking
CF_User_Rank_Weight = 0.9
CF_Item_Rank_Weight = 1
CB_User_Rank_Weight = 0.5
CB_Item_Rank_Weight = 1
CB_CF_IB_Hybrid_Rank_Weight = 1
CB_IB_CF_IB_UB_Hybrid_Rank_Weight = 4
ML_SVD_Rank_Weight = 0

#timestamp of the fifth day before the last interaction
timestamp_last_three_days = 1446681600
timestamp_last_five_days = 1446508800
timestamp_last_seven_days = 1446336000
timestamp_last_ten_days = 1446076800

#Dictionary for number of click on items
item_number_click_dictionary = {}

#Creating the dictionary which collect for each item the number of times it has been clicked by the users
for user, item, interaction, created in interactions.values:
    if (created >= timestamp_last_seven_days):
        if item_number_click_dictionary.has_key(item):
            item_number_click_dictionary[item] += 1
        else:
            item_number_click_dictionary[item] = 1

# return the max number of click on an item in the last 5 days
max_click = 0
for item in item_number_click_dictionary:
    max_click = max(max_click, item_number_click_dictionary[item])

CB_UB_users_prediction_dictionary_normalized = CBAlgorithms.CBRead_Predictions(CB_UB_predictions_output)
CB_IB_users_prediction_dictionary_normalized = CBAlgorithms.CBRead_Predictions(CB_IB_predictions_output)
CF_HB_UB_users_prediction_dictionary_normalized = CFAlgorithms.CFRead_Predictions(CF_UB_predictions_output)
CF_HB_IB_users_prediction_dictionary_normalized = CFAlgorithms.CFRead_Predictions(CF_IB_predictions_output)
ML_SVD_user_prediction_dictionary = MLAlgorithms.MLRead_Predictions(ML_SVD_predictions_output)

#CBAlgorithms.CBWriteResult(CB_UB_MAP_Output, CB_UB_users_prediction_dictionary_normalized)
#CBAlgorithms.CBWriteResult(CB_IB_MAP_Output, CB_IB_users_prediction_dictionary_normalized)
#CFAlgorithms.CFWriteResult(CF_HB_UB_MAP_Output, CF_HB_UB_users_prediction_dictionary_normalized)
#CFAlgorithms.CFWriteResult(CF_HB_IB_MAP_Output, CF_HB_IB_users_prediction_dictionary_normalized)
#MLAlgorithms.MLWriteResult(ML_SVD_MAP_Output, ML_SVD_user_prediction_dictionary)

#Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBIB-CFIB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_HB_UB_users_prediction_dictionary_normalized,
                                                                                                               CF_HB_IB_users_prediction_dictionary_normalized,
                                                                                                               CF_User_Rank_Weight, CF_Item_Rank_Weight)

del CF_HB_UB_users_prediction_dictionary_normalized
del CF_HB_IB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBCFIB-CFUB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CB_IB_users_prediction_dictionary_normalized,
                                                                                                               CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CB_Item_Rank_Weight, CB_CF_IB_Hybrid_Rank_Weight)

del CB_IB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBIBCFIBUB-CBUB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CB_UB_users_prediction_dictionary_normalized,
                                                                                                               CB_IB_CF_IB_UB_Hybrid_Rank_Weight, CB_User_Rank_Weight)

del CB_UB_users_prediction_dictionary_normalized

HB_CF_CB_ML_users_prediction_dictionary = MLAlgorithms.MLHybridPredictNormalizedRecommendation(CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                               ML_SVD_user_prediction_dictionary, ML_SVD_Rank_Weight)

final_users_prediction_dictionary = CFAlgorithms.CF_Popularity_Rank_Predictions(HB_CF_CB_ML_users_prediction_dictionary,
                                                                                item_number_click_dictionary, max_click)
# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_CB_ML_Hybrid_MAP_Output, final_users_prediction_dictionary)

# Compute the LocalMAP@5
#va.MAP(target_users, validation, CB_UB_MAP_Output)
#va.MAP(target_users, validation, CB_IB_MAP_Output)
#va.MAP(target_users, validation, CF_HB_UB_MAP_Output)
#va.MAP(target_users, validation, CF_HB_IB_MAP_Output)
#va.MAP(target_users, validation, ML_Funk_SVD_MAP_Output)
va.MAP(target_users, validation, CF_HB_UB_MAP_Output)