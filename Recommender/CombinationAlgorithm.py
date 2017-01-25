import CBAlgorithms
import CFAlgorithms
import pandas as pd

cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('../DataSet/interactions.csv', sep='\t', names=cols, header=0)

# Filename for the output result
CB_UB_predictions_output = "../Predictions/CB_User_Based.csv"
CB_IB_predictions_output = "../Predictions/CB_Item_Based.csv"
CF_UB_predictions_output = "../Predictions/CF_User_Based.csv"
CF_IB_predictions_output = "../Predictions/CF_Item_Based.csv"

CF_Hybrid_Ranked_Output = "../Results/CF_Hybrid_Ranked.csv"

# Weight values for Collaborative Filtering, Content Based and Hybrid Ranking
CF_User_Rank_Weight = 0.9
CF_Item_Rank_Weight = 1
CB_User_Rank_Weight = 0.5
CB_Item_Rank_Weight = 1
CF_UB_IB_Hybrid_Rank_Weight = 1
CB_IB_CF_IB_UB_Hybrid_Rank_Weight = 4

# timestamp of the fifth day before the last interaction
timestamp_last_five_day = 1446508800

# Dictionary for number of click on items
item_number_click_dictionary = {}

# Creating the dictionary which collect for each item the number of times it has been clicked by the users
for user, item, interaction, created in interactions.values:
    if (created >= timestamp_last_five_day):
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

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CFUB-CFIB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_HB_UB_users_prediction_dictionary_normalized,
                                                                                                               CF_HB_IB_users_prediction_dictionary_normalized,
                                                                                                               CF_User_Rank_Weight, CF_Item_Rank_Weight)

del CF_HB_UB_users_prediction_dictionary_normalized
del CF_HB_IB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CFUBIB-CBIB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CB_IB_users_prediction_dictionary_normalized,
                                                                                                               CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CB_Item_Rank_Weight, CF_UB_IB_Hybrid_Rank_Weight)

del CB_IB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBIBCFIBUB-CBUB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CB_UB_users_prediction_dictionary_normalized,
                                                                                                               CB_IB_CF_IB_UB_Hybrid_Rank_Weight, CB_User_Rank_Weight)

del CB_UB_users_prediction_dictionary_normalized


final_users_prediction_dictionary = CFAlgorithms.CF_Popularity_Rank_Predictions(CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                item_number_click_dictionary, max_click)

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_Hybrid_Ranked_Output, final_users_prediction_dictionary)