from __future__ import division
from collections import OrderedDict

def MLHybridPredictNormalizedRecommendation(actual_users_prediction_dictionary, ML_user_prediction_dictionary, ML_Weight):
    max_prediction = 0
    for user in ML_user_prediction_dictionary:
        max_prediction = 0
        for item in ML_user_prediction_dictionary[user]:
            max_prediction = max(max_prediction, ML_user_prediction_dictionary[user][item])
        if not actual_users_prediction_dictionary.has_key(user):
            actual_users_prediction_dictionary[user] = {}
        for item in ML_user_prediction_dictionary[user]:
            if actual_users_prediction_dictionary[user].has_key(item):
                actual_users_prediction_dictionary[user][item] += (ML_user_prediction_dictionary[user][item] * ML_Weight) / max_prediction
            else:
                actual_users_prediction_dictionary[user][item] = (ML_user_prediction_dictionary[user][item] * ML_Weight) / max_prediction

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

# Function to write the final result of recommendation
def MLWriteResult(output_filename, users_prediction_dictionary):
    sum = 0
    print ("Writing result on " + output_filename)
    out_file = open(output_filename, "w")
    out_file.write('user_id,recommended_items\n')
    for user in users_prediction_dictionary:
        if len(users_prediction_dictionary[user].keys()) > 0:
            users_prediction_dictionary[user] = OrderedDict(
                sorted(users_prediction_dictionary[user].items(), key=lambda t: -t[1]))
        x = users_prediction_dictionary[user].keys()
        x = map(str, x)
        out_file.write(str(user) + ',' + ' '.join(x[:min(len(x), 5)]) + '\n')
        sum += min(len(x), 5)
    left = 50000 - sum
    print(str(left) + " item(s) left in the result")
    out_file.close()