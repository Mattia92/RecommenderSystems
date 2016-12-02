from __future__ import division
import pandas as pd
import os

def apk(actual, predicted, k):
    # Initialize all the variables needed
    sum = 0.0
    rec_new = 0.0
    k1 = min(min(k, len(predicted)), len(actual))
    # For each index from 1 to 5 (length of the predicted list if it is less than 5)
    for i in range(1, k1+1):
        # Numbers of correct predictions
        good_pred = 0
        # For each prediction to consider at point i find the number of good predictions
        for p in predicted[:i]:
            if p in actual:
                good_pred += 1
        # Compute the Precision at time i
        prec = good_pred / i
        # Compute the Recall at time i-1
        rec_old = rec_new
        # Compute the Recall at time i
        rec_new = good_pred / len(actual)
        # Compute the Average Precision at k
        sum += prec * (rec_new - rec_old)

    return sum

def MAP(target_users, validation, result_filename):
    result = pd.read_csv(result_filename, sep=',', header=0)

    # Creating Validation dictionary and Result dictionary
    validation_dictionary = {}
    result_dictionary = {}

    # Create the dictionaries needed to compute the local MAP@5
    # Dictionary is a list of elements, each element is defined as following
    # dict {user -> (list of recommended items)}
    print ("Create dictionaries for validation and result")
    for user, items in validation.values:
        if user in target_users['user_id'].values:
            validation_dictionary[user] = items.split()

    for user, items in result.values:
        if (pd.isnull(items)):
            result_dictionary[user] = []
        else:
            item = str(items)
            result_dictionary[user] = item.split()

    print ("Compute the local MAP@5")
    av_prec = 0
    # For each user in the validation dictionary
    for user in validation_dictionary:
        # If the user is not inside the result dictionary continue
        if not result_dictionary.has_key(user):
            continue
        # Else compute the Average Precision for that user
        av_prec += apk(validation_dictionary[user], result_dictionary[user], 5)

    # Compute the local Mean Average Precision
    map_at = av_prec / len(validation_dictionary)
    map_at = round(map_at,5)
    print (result_filename + " MAP@5: " + str(map_at * 100000))

    # Remove the output csv file
    os.remove(result_filename)