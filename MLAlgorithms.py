def MLHybridPredictNormalizedRecommendation(actual_users_prediction_dictionary, SVD_user_prediction_dictionary, ML_SVD_Weight):
    for user in SVD_user_prediction_dictionary:
        if not actual_users_prediction_dictionary.has_key(user):
            actual_users_prediction_dictionary[user] = {}
        for item in SVD_user_prediction_dictionary[user]:
            if actual_users_prediction_dictionary[user].has_key(item):
                actual_users_prediction_dictionary[user][item] += SVD_user_prediction_dictionary[user][item] * ML_SVD_Weight
            else:
                actual_users_prediction_dictionary[user][item] = SVD_user_prediction_dictionary[user][item] * ML_SVD_Weight

    return actual_users_prediction_dictionary

def MLRead_Predictions(output_filename):
    print ("Reading predictions from " + output_filename)
    in_file = open(output_filename, "r")
    users_prediction_dictionary = {}
    for line in in_file:
        line = line.strip('\n')
        predictions = line.split("\t")
        if not(users_prediction_dictionary.has_key(predictions[0])):
            users_prediction_dictionary[predictions[0]] = {}
        users_prediction_dictionary[predictions[0]][predictions[1]] = float(predictions[2])
    in_file.close()
    return users_prediction_dictionary