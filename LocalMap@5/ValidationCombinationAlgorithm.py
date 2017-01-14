import CBAlgorithms
import CFAlgorithms
import pandas as pd
import ValidationAlgorithm as va

target_users = pd.read_csv('../DataSet/target_users.csv')
validation = pd.read_csv('../TestDataSet/validationSet.csv', sep=',', header=0)

# Filename for the output result
CB_UB_predictions_output = "../ValidationPredictions/Validation_CB_User_Based.csv"
CB_IB_predictions_output = "../ValidationPredictions/Validation_CB_Item_Based.csv"
CF_UB_predictions_output = "../ValidationPredictions/Validation_CF_User_Based.csv"
CF_IB_predictions_output = "../ValidationPredictions/Validation_CF_Item_Based.csv"

# Filename for the output result
CB_UB_MAP_Output = "../TestDataSet/CB_MAP_User_Based.csv"
CB_IB_MAP_Output = "../TestDataSet/CB_MAP_Item_Based.csv"
CF_HB_UB_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_User_Based.csv"
CF_HB_IB_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_Item_Based.csv"
CF_Hybrid_Ranked_MAP_Output = "../TestDataSet/CF_MAP_Hybrid_Ranked.csv"

# Weight values for Collaborative Filtering, Content Based and Hybrid Ranking
CF_User_Rank_Weight = 0.5
CF_Item_Rank_Weight = 1
CB_User_Rank_Weight = 0.5
CB_Item_Rank_Weight = 0.5
CB_CF_IB_Hybrid_Rank_Weight = 1
CB_IB_CF_IB_UB_Hybrid_Rank_Weight = 4

CB_UB_users_prediction_dictionary_normalized = CBAlgorithms.CBRead_Predictions(CB_UB_predictions_output)
CB_IB_users_prediction_dictionary_normalized = CBAlgorithms.CBRead_Predictions(CB_IB_predictions_output)
CF_HB_UB_users_prediction_dictionary_normalized = CFAlgorithms.CFRead_Predictions(CF_UB_predictions_output)
CF_HB_IB_users_prediction_dictionary_normalized = CFAlgorithms.CFRead_Predictions(CF_IB_predictions_output)

#CBAlgorithms.CBWriteResult(CB_UB_MAP_Output, CB_UB_users_prediction_dictionary_normalized)
#CBAlgorithms.CBWriteResult(CB_IB_MAP_Output, CB_IB_users_prediction_dictionary_normalized)
#CFAlgorithms.CFWriteResult(CF_HB_UB_MAP_Output, CF_HB_UB_users_prediction_dictionary_normalized)
#CFAlgorithms.CFWriteResult(CF_HB_IB_MAP_Output, CF_HB_IB_users_prediction_dictionary_normalized)

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBIB-CFIB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CB_IB_users_prediction_dictionary_normalized,
                                                                                                               CF_HB_IB_users_prediction_dictionary_normalized,
                                                                                                               CB_Item_Rank_Weight, CF_Item_Rank_Weight)

del CB_IB_users_prediction_dictionary_normalized
del CF_HB_IB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBCFIB-CFUB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_HB_UB_users_prediction_dictionary_normalized,
                                                                                                               CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CF_User_Rank_Weight, CB_CF_IB_Hybrid_Rank_Weight)

del CF_HB_UB_users_prediction_dictionary_normalized

# Compute the Prediction for Normalized Collaborative Filtering and Content Based Hybrid Rank (CBIBCFIBUB-CBUB)
CF_Normalized_HB_Ranked_users_prediction_dictionary = CFAlgorithms.CFHybridRankPredictNormalizedRecommendation(CF_Normalized_HB_Ranked_users_prediction_dictionary,
                                                                                                               CB_UB_users_prediction_dictionary_normalized,
                                                                                                               CB_IB_CF_IB_UB_Hybrid_Rank_Weight, CB_User_Rank_Weight)

del CB_UB_users_prediction_dictionary_normalized

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_Hybrid_Ranked_MAP_Output, CF_Normalized_HB_Ranked_users_prediction_dictionary)

# Compute the LocalMAP@5
#va.MAP(target_users, validation, CB_UB_MAP_Output)
#va.MAP(target_users, validation, CB_IB_MAP_Output)
#va.MAP(target_users, validation, CF_HB_UB_MAP_Output)
#va.MAP(target_users, validation, CF_HB_IB_MAP_Output)
va.MAP(target_users, validation, CF_Hybrid_Ranked_MAP_Output)