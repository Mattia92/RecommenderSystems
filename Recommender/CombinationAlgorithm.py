import CBAlgorithms
import CFAlgorithms

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

# Write the final Result for Collaborative Filtering Hybrid Rank
CFAlgorithms.CFWriteResult(CF_Hybrid_Ranked_Output, CF_Normalized_HB_Ranked_users_prediction_dictionary)