import math
from collections import OrderedDict

# Function to build the User-User Similarity Dictionary
def CFUserUserSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_user_similarity_dictionary_den1 = {}
    user_user_similarity_dictionary_den2 = {}
    print ("Create dictionaries for CF user-user similarity")
    # For each user in the dictionary
    for user in user_items_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        interacted_items = user_items_dictionary[user]
        # For each item in the dictionary pointed by the user
        for item in interacted_items:
            # Get the dictionary pointed by the item, containing the users which have interact with the item
            interacted_users = item_users_dictionary[item]
            # Get list of users which have interacted with the same item of the first user
            user_list = interacted_users.keys()
            # Instantiate the similarity dictionary
            # dict {user -> (dict2)}
            # dict2 will be {similar_user -> similarity}
            user_user_similarity_dictionary_num[user] = {}
            user_user_similarity_dictionary_den1[user] = {}
            user_user_similarity_dictionary_den2[user] = {}
            # For each user in the list of users
            for list_element in user_list:
                # If similar_user is already in dict2 create the sum of product of ratings
                if (user_user_similarity_dictionary_num[user].has_key(list_element)):
                    user_user_similarity_dictionary_num[user][list_element] += interacted_items[item] * \
                                                                               user_items_dictionary[list_element][item]
                    user_user_similarity_dictionary_den1[user][list_element] += math.pow(interacted_items[item], 2)
                    user_user_similarity_dictionary_den2[user][list_element] += math.pow(
                        user_items_dictionary[list_element][item], 2)
                # Else the similar_user and the product of ratings are added to dict2
                else:
                    user_user_similarity_dictionary_num[user][list_element] = interacted_items[item] * \
                                                                              user_items_dictionary[list_element][item]
                    user_user_similarity_dictionary_den1[user][list_element] = math.pow(interacted_items[item], 2)
                    user_user_similarity_dictionary_den2[user][list_element] = math.pow(
                        user_items_dictionary[list_element][item], 2)
                    # Remove from similar_users the user itself
        if (user_user_similarity_dictionary_num[user].has_key(user)):
            del user_user_similarity_dictionary_num[user][user]
            del user_user_similarity_dictionary_den1[user][user]
            del user_user_similarity_dictionary_den2[user][user]

    print ("Similarities estimate:")
    # For each user (user_user_similarity_dictionary_num contains all users which have at least one interaction)
    for user in user_user_similarity_dictionary_num:
        user_user_similarity_dictionary[user] = {}
        # For each similar user for the user
        for user2 in user_user_similarity_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            user_user_similarity_dictionary[user][user2] = user_user_similarity_dictionary_num[user][user2] / \
                                                           ((math.sqrt(
                                                               user_user_similarity_dictionary_den1[user][user2]) *
                                                             math.sqrt(
                                                                 user_user_similarity_dictionary_den2[user][user2])) +
                                                            similarity_shrink)

    return user_user_similarity_dictionary

# Function to create the recommendations
def CFPredictRecommendation(target_users, user_user_similarity_dictionary, user_items_dictionary, prediction_shrink):
    print ("Create dictionaries for CF user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for user in target_users['user_id']:
        users_prediction_dictionary_num[user] = {}
        users_prediction_dictionary_den[user] = {}
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
                        users_prediction_dictionary_den[user][i] = uus_list[user2]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[user][i] += uus_list[user2] * u2_item_list[i]
                        users_prediction_dictionary_den[user][i] += uus_list[user2]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                      (users_prediction_dictionary_den[user][item] + prediction_shrink)

    return users_prediction_dictionary

# Function to write the final result of recommendation
def CFWriteResult(output_filename, users_prediction_dictionary):
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

    out_file.close()