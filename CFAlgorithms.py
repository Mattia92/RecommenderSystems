from __future__ import division
import math
from collections import OrderedDict

# Function to build the User-User Similarity Dictionary
def CFUserUserSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_similarity_dictionary_norm = {}
    print ("Create dictionaries for CF user-user similarity")
    # For each user in the dictionary
    for user in user_items_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        interacted_items = user_items_dictionary[user]
            # Instantiate the similarity dictionary
            # dict {user -> (dict2)}
            # dict2 will be {similar_user -> similarity}
        user_user_similarity_dictionary_num[user] = {}
        # For each item in the dictionary pointed by the user
        for item in interacted_items:
            # Get the dictionary pointed by the item, containing the users which have interact with the item
            interacted_users = item_users_dictionary[item]
            # Get list of users which have interacted with the same item of the first user
            user_list = interacted_users.keys()
            # For each user in the list of users
            for list_element in user_list:
                # If similar_user is already in dict2 create the sum of product of ratings
                if (user_user_similarity_dictionary_num[user].has_key(list_element)):
                    user_user_similarity_dictionary_num[user][list_element] += interacted_items[item] * \
                                                                               user_items_dictionary[list_element][item]
                # Else the similar_user and the product of ratings are added to dict2
                else:
                    user_user_similarity_dictionary_num[user][list_element] = interacted_items[item] * \
                                                                              user_items_dictionary[list_element][item]
        # Remove from similar_users the user itself
        if (user_user_similarity_dictionary_num[user].has_key(user)):
            del user_user_similarity_dictionary_num[user][user]

    # For each user in the dictionary
    for user in user_items_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        interacted_items = user_items_dictionary[user]
        user_similarity_dictionary_norm[user] = math.sqrt(len(interacted_items))


    print ("Similarities estimate:")
    # For each user (user_user_similarity_dictionary_num contains all users which have at least one interaction)
    for user in user_user_similarity_dictionary_num:
        user_user_similarity_dictionary[user] = {}
        # For each similar user for the user
        for user2 in user_user_similarity_dictionary_num[user]:
            # Evaluate the similarity between user and user2
            user_user_similarity_dictionary[user][user2] = user_user_similarity_dictionary_num[user][user2] / \
                                                           ((user_similarity_dictionary_norm[user] * user_similarity_dictionary_norm[user2]) +
                                                            similarity_shrink)

    return user_user_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CFItemItemSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    item_item_similarity_dictionary = {}
    item_item_similarity_dictionary_num = {}
    item_similarity_dictionary_norm = {}
    print ("Create dictionaries for CF item-item similarity")
    # For each item in the dictionary
    for item in item_users_dictionary:
        # Get the dictionary pointed by the item, containing the users which has interact with that item
        interacting_users = item_users_dictionary[item]
            # Instantiate the similarity dictionary
            # dict {item -> (dict2)}
            # dict2 will be {similar_item -> similarity}
        item_item_similarity_dictionary_num[item] = {}
        # For each user in the dictionary pointed by the item
        for user in interacting_users:
            # Get the dictionary pointed by the user, containing the items with which the user has interact
            interacted_items = user_items_dictionary[user]
            # Get list of items with which this user has interact
            item_list = interacted_items.keys()
            # For each item in the list of items
            for list_element in item_list:
                # If similar_item is already in dict2 create the sum of product of ratings
                if (item_item_similarity_dictionary_num[item].has_key(list_element)):
                    item_item_similarity_dictionary_num[item][list_element] += interacting_users[user] * interacted_items[list_element]
                # Else the similar_item is added to dict2 and the product of ratings is set to 1
                else:
                    item_item_similarity_dictionary_num[item][list_element] = interacting_users[user] * interacted_items[list_element]
        # Remove from similar_items the item itself
        if (item_item_similarity_dictionary_num[item].has_key(item)):
            del item_item_similarity_dictionary_num[item][item]
    # For each user in the dictionary
    for item in item_users_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        interact_users = item_users_dictionary[item]
        item_similarity_dictionary_norm[item] = math.sqrt(len(interact_users))

    print ("Similarities estimate:")
    # For each item (item_item_similarity_dictionary_num contains all items which have at least one interaction)
    # Evaluate the value of similarity
    for item in item_item_similarity_dictionary_num:
        item_item_similarity_dictionary[item] = {}
        # For each similar item for the item
        for item2 in item_item_similarity_dictionary_num[item]:
            # Evaluate the similarity between item and item2
            item_item_similarity_dictionary[item][item2] = item_item_similarity_dictionary_num[item][item2] / \
                                                           ((item_similarity_dictionary_norm[item] * item_similarity_dictionary_norm[item2]) +
                                                            similarity_shrink)

    return item_item_similarity_dictionary

# Function to create the recommendations for User_Based
def CFUserBasedPredictRecommendation(target_users, user_user_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                     prediction_shrink):
    print ("Create dictionaries for CF User Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users['user_id']:
        users_prediction_dictionary_num[user] = {}
        # If user has similar users
        if (user_user_similarity_dictionary.has_key(user)):
            # Get dictionary of similar users and the value of similarity
            uus_list = user_user_similarity_dictionary[user]
            # For each similar user in the dictionary
            for user2 in uus_list:
                # Get the dictionary of items with which this user has interact
                u2_item_list = user_items_dictionary[user2]
                # For each item in the dictionary
                for i in u2_item_list:
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[user].has_key(i)):
                        users_prediction_dictionary_num[user][i] = uus_list[user2] * u2_item_list[i]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[user][i] += uus_list[user2] * u2_item_list[i]

    # For each user in the dictionary
    for user in user_user_similarity_dictionary:
        users_prediction_dictionary_norm[user] = 0
        # Get the dictionary pointed by the user, containing the similar users
        sim_users = user_user_similarity_dictionary[user]
        for other_user in sim_users:
            users_prediction_dictionary_norm[user] += sim_users[other_user]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            if not (item in user_items_dictionary[user]):
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)

    return users_prediction_dictionary

# Function to create the recommendations for Item_Based
def CFItemBasedPredictRecommendation(target_users, item_item_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                     prediction_shrink):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users['user_id']:
        users_prediction_dictionary_num[user] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(user)):
            # Get dictionary of items with which the user has interact
            i_list = user_items_dictionary[user]
            # For each item in this dictionary
            for item in i_list:
                # Get the dictionary of similar items and the value of similarity
                iis_list = item_item_similarity_dictionary[item]
                # For each similar item in the dictionary
                for item2 in iis_list:
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[user].has_key(item2)):
                        users_prediction_dictionary_num[user][item2] = iis_list[item2] * i_list[item]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[user][item2] += iis_list[item2] * i_list[item]

    # For each user in the dictionary
    for item in item_item_similarity_dictionary:

        users_prediction_dictionary_norm[item] = 0
        # Get the dictionary pointed by the item, containing the similar items
        sim_items = item_item_similarity_dictionary[item]
        for other_item in sim_items:
            users_prediction_dictionary_norm[item] += sim_items[other_item]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            if not (item in user_items_dictionary[user]):
                if (active_items_to_recommend.has_key(item)):
                    if not (users_prediction_dictionary_norm[item] == 0):
                        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[item] + prediction_shrink)

    return users_prediction_dictionary

# Function to create the recommendations for Hybrid Weighted
def CFHybridWeightedPredictRecommendation(user_based_users_prediction, item_based_users_predictions, weight):
    users_prediction_dictionary = {}
    # For each user in the User_Based Prediction
    for user in user_based_users_prediction:
        users_prediction_dictionary[user] = {}
        # For each item in the User_Based Prediction
        for item in user_based_users_prediction[user]:
            # Compute the weighted prediction value
            users_prediction_dictionary[user][item] = user_based_users_prediction[user][item] * weight

    # For each user in the Item_Based Prediction
    for user in item_based_users_predictions:
        # For each item in the Item_Based Prediction
        for item in item_based_users_predictions[user]:
            # If the item was already predicted for that user in the User_Based Algorithm
            if (users_prediction_dictionary[user].has_key(item)):
                # Compute the weighted prediction value adding the prediction value computed by the Item_Based Algorithm
                users_prediction_dictionary[user][item] += item_based_users_predictions[user][item] * (1 - weight)
            else:
                # Compute the weighted prediction value
                users_prediction_dictionary[user][item] = item_based_users_predictions[user][item] * (1 - weight)

    return users_prediction_dictionary

# Function to create the recommendations for Hybrid Rank
def CFHybridRankPredictRecommendation(user_based_users_prediction, item_based_users_predictions, items_to_consider,
                                      user_based_weight, item_based_weight):
    users_prediction_dictionary = {}
    #for each user in User Based prediction
    for user in user_based_users_prediction:
        # if there is at least one prediction for the user sort the predictions
        if len(user_based_users_prediction[user].keys()) > 0:
            user_based_users_prediction[user] = OrderedDict(
            sorted(user_based_users_prediction[user].items(), key=lambda t: -t[1]))
    #for each user in Item Based prediction
    for user in item_based_users_predictions:
        # if there is at least one prediction for the user sort the predictions
        if len(item_based_users_predictions[user].keys()) > 0:
            item_based_users_predictions[user] = OrderedDict(
            sorted(item_based_users_predictions[user].items(), key=lambda t: -t[1]))
    # for each user in the User based prediction
    for user in user_based_users_prediction:
        k = 0   # k represent the rank position of the item in the user predictions
        UB_size = min(len(user_based_users_prediction[user]), items_to_consider)
        users_prediction_dictionary[user] = {}
        # for each item in the User based prediction
        for item in user_based_users_prediction[user]:
            # if the position of the item is less than the number of items to consider assign the value to the new dictionary
            if (k < items_to_consider):
                users_prediction_dictionary[user][item] = user_based_weight * ( 1 - ( k / UB_size ) )
                k += 1
            else:
                break
    # for each user in the Item based prediction
    for user in item_based_users_predictions:
        k = 0   # k represents the rank position of the item in the user predictions
        IB_size = min(len(item_based_users_predictions[user]), items_to_consider)
        for item in item_based_users_predictions[user]:
            # if the position of the item is less than the number of items to consider assign the value to the dictionary
            if (k < items_to_consider):
                # if the item is already present in the user predictions sum the two values
                if (users_prediction_dictionary[user].has_key(item)):
                    users_prediction_dictionary[user][item] += item_based_weight * ( 1 - ( k / IB_size ) )
                    k += 1
                # else assign the value to the item
                else:
                    users_prediction_dictionary[user][item] = item_based_weight * ( 1 - ( k / IB_size ) )
                    k += 1
            else:
                break

    return users_prediction_dictionary

# Function to write the final result of recommendation
def CFWriteResult(output_filename, users_prediction_dictionary):
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