from __future__ import division
import math
import operator
from collections import OrderedDict

# Function to compute Items IDF
def CF_IDF(interactions):
    print ("Create dictionary for CF_IDF")
    CF_IB_IDF = {}
    item_num_interactions = {}
    for user, item, interaction in interactions.values:
        item_num_interactions[item] = 0
    for user, item, interaction in interactions.values:
        item_num_interactions[item] += 1
    for user, item, interaction in interactions.values:
        CF_IB_IDF[item] = math.log10(len(interactions) / item_num_interactions[item])

    return CF_IB_IDF

# Function to build the User-User Similarity Dictionary
def CFUserUserSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink, KNN):
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

    if (KNN == 0):
        return user_user_similarity_dictionary
    else:
        user_user_KNN_similarity_dictionary = {}
        for user in user_user_similarity_dictionary:
            user_user_KNN_similarity_dictionary[user] = {}
            KNN_sim_users = sorted(user_user_similarity_dictionary[user].items(), key=operator.itemgetter(1))
            KNN_sim_users_desc = sorted(KNN_sim_users, key=lambda tup: -tup[1])
            for sim_user in KNN_sim_users_desc:
                if (len(user_user_KNN_similarity_dictionary[user]) < KNN):
                    user_user_KNN_similarity_dictionary[user][sim_user[0]] = user_user_similarity_dictionary[user][sim_user[0]]

        return user_user_KNN_similarity_dictionary

# Function to build the User-User Similarity Dictionary
def CFHybridUserUserSimilarity(user_items_dictionary, item_users_dictionary, users_attributes_dictionary, CF_similarity_shrink,
                               CB_similarity_shrink, KNN, w):
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
                                                           ((user_similarity_dictionary_norm[user] *
                                                             user_similarity_dictionary_norm[user2]) +
                                                            CF_similarity_shrink)

    print ("Combine CB and CF Similarities:")
    CB_similarity_num = {}
    CB_similarity_norm = {}
    CB_similarity_dict = {}
    for user in user_user_similarity_dictionary:
        CB_similarity_num[user] = {}
        similar_users = user_user_similarity_dictionary[user]
        att_u = users_attributes_dictionary[user]
        for user2 in similar_users:
            att_u2 = users_attributes_dictionary[user2]
            for attribute in att_u:
                if (att_u2.has_key(attribute)):
                    if (CB_similarity_num[user].has_key(user2)):
                        CB_similarity_num[user][user2] += users_attributes_dictionary[user][attribute] * \
                                                      users_attributes_dictionary[user2][attribute]
                    else:
                        CB_similarity_num[user][user2] = users_attributes_dictionary[user][attribute] * \
                                                     users_attributes_dictionary[user2][attribute]

    for user in CB_similarity_num:
        # For each attribute of the user
        for attribute in users_attributes_dictionary[user]:
            # Calculate the norm of the vector corresponding to the user attributes
            if (CB_similarity_norm.has_key(user)):
                CB_similarity_norm[user] += math.pow(users_attributes_dictionary[user][attribute], 2)
            else:
                CB_similarity_norm[user] = math.pow(users_attributes_dictionary[user][attribute], 2)
        CB_similarity_norm[user] = math.sqrt(CB_similarity_norm[user])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for user in CB_similarity_num:
        CB_similarity_dict[user] = {}
        # Calculate the user-user similarity
        for user_j in CB_similarity_num[user]:
            CB_similarity_dict[user][user_j] = CB_similarity_num[user][user_j] / (CB_similarity_norm[user] *
                                                                                  CB_similarity_norm[user_j] +
                                                                                  CB_similarity_shrink)

    print ("Similarities combination:")
    for user in user_user_similarity_dictionary:
        similar_users = user_user_similarity_dictionary[user]
        for user2 in similar_users:
            if (CB_similarity_dict[user].has_key(user2)):
                user_user_similarity_dictionary[user][user2] += (w * CB_similarity_dict[user][user2])

    if (KNN == 0):
        return user_user_similarity_dictionary
    else:
        user_user_KNN_similarity_dictionary = {}
        for user in user_user_similarity_dictionary:
            user_user_KNN_similarity_dictionary[user] = {}
            KNN_sim_users = sorted(user_user_similarity_dictionary[user].items(), key=operator.itemgetter(1))
            KNN_sim_users_desc = sorted(KNN_sim_users, key=lambda tup: -tup[1])
            for sim_user in KNN_sim_users_desc:
                if (len(user_user_KNN_similarity_dictionary[user]) < KNN):
                    user_user_KNN_similarity_dictionary[user][sim_user[0]] = user_user_similarity_dictionary[user][
                        sim_user[0]]

        return user_user_KNN_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CFItemItemSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink, KNN):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    item_item_similarity_dictionary = {}
    item_item_similarity_dictionary_num = {}
    item_similarity_dictionary_norm = {}
    print ("Create dictionaries for CF item-item similarity")
    # For each item in the dictionary
    for ii in item_users_dictionary:
        # Get the dictionary pointed by the item, containing the users which has interact with that item
        u_r_dict = item_users_dictionary[ii]
        # Instantiate the similarity dictionary
        # dict {item -> (dict2)}
        # dict2 will be {similar_item -> similarity}
        item_item_similarity_dictionary_num[ii] = {}
        # For each user in the dictionary pointed by the item
        for u in u_r_dict:
            # Get the dictionary pointed by the user, containing the items with which the user has interact
            i_r_dict = user_items_dictionary[u]
            # For each item in the list of items
            for ij in i_r_dict:
                if (ij == ii):
                    continue
                # If similar_item is already in dict2 create the sum of product of ratings
                if (item_item_similarity_dictionary_num[ii].has_key(ij)):
                    item_item_similarity_dictionary_num[ii][ij] += i_r_dict[ii] * i_r_dict[ij]
                # Else the similar_item is added to dict2 and the product of ratings is set to 1
                else:
                    item_item_similarity_dictionary_num[ii][ij] = i_r_dict[ii] * i_r_dict[ij]
    # For each user in the dictionary
    for i in item_users_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        u_r_dict = item_users_dictionary[i]
        item_similarity_dictionary_norm[i] = math.sqrt(len(u_r_dict))

    print ("Similarities estimate:")
    # For each item (item_item_similarity_dictionary_num contains all items which have at least one interaction)
    # Evaluate the value of similarity
    for ii in item_item_similarity_dictionary_num:
        item_item_similarity_dictionary[ii] = {}
        # For each similar item for the item
        for ij in item_item_similarity_dictionary_num[ii]:
            # Evaluate the similarity between item and item2
            item_item_similarity_dictionary[ii][ij] = item_item_similarity_dictionary_num[ii][ij] / \
                                                           ((item_similarity_dictionary_norm[ii] * item_similarity_dictionary_norm[ij]) +
                                                            similarity_shrink)

    if (KNN == 0):
        return item_item_similarity_dictionary
    else:
        item_item_KNN_similarity_dictionary = {}
        for item in item_item_similarity_dictionary:
            item_item_KNN_similarity_dictionary[item] = {}
            KNN_sim_items = sorted(item_item_similarity_dictionary[item].items(), key=operator.itemgetter(1))
            KNN_sim_items_desc = sorted(KNN_sim_items, key=lambda tup: -tup[1])
            for sim_item in KNN_sim_items_desc:
                if (len(item_item_KNN_similarity_dictionary[item]) < KNN):
                    item_item_KNN_similarity_dictionary[item][sim_item[0]] = item_item_similarity_dictionary[item][sim_item[0]]

        return item_item_KNN_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CFHybridItemItemSimilarity(user_items_dictionary, item_users_dictionary, items_attributes_dictionary, CF_similarity_shrink,
                               CB_similarity_shrink, KNN, w):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    item_item_similarity_dictionary = {}
    item_item_similarity_dictionary_num = {}
    item_similarity_dictionary_norm = {}
    print ("Create dictionaries for CF item-item similarity")
    # For each item in the dictionary
    for ii in item_users_dictionary:
        # Get the dictionary pointed by the item, containing the users which has interact with that item
        u_r_dict = item_users_dictionary[ii]
        # Instantiate the similarity dictionary
        # dict {item -> (dict2)}
        # dict2 will be {similar_item -> similarity}
        item_item_similarity_dictionary_num[ii] = {}
        # For each user in the dictionary pointed by the item
        for u in u_r_dict:
            # Get the dictionary pointed by the user, containing the items with which the user has interact
            i_r_dict = user_items_dictionary[u]
            # For each item in the list of items
            for ij in i_r_dict:
                if (ij == ii):
                    continue
                # If similar_item is already in dict2 create the sum of product of ratings
                if (item_item_similarity_dictionary_num[ii].has_key(ij)):
                    item_item_similarity_dictionary_num[ii][ij] += i_r_dict[ii] * i_r_dict[ij]
                # Else the similar_item is added to dict2 and the product of ratings is set to 1
                else:
                    item_item_similarity_dictionary_num[ii][ij] = i_r_dict[ii] * i_r_dict[ij]
    # For each user in the dictionary
    for i in item_users_dictionary:
        # Get the dictionary pointed by the user, containing the items with which the user has interact
        u_r_dict = item_users_dictionary[i]
        item_similarity_dictionary_norm[i] = math.sqrt(len(u_r_dict))

    print ("Similarities estimate:")
    # For each item (item_item_similarity_dictionary_num contains all items which have at least one interaction)
    # Evaluate the value of similarity
    for ii in item_item_similarity_dictionary_num:
        item_item_similarity_dictionary[ii] = {}
        # For each similar item for the item
        for ij in item_item_similarity_dictionary_num[ii]:
            # Evaluate the similarity between item and item2
            item_item_similarity_dictionary[ii][ij] = item_item_similarity_dictionary_num[ii][ij] / \
                                                      ((item_similarity_dictionary_norm[ii] *
                                                        item_similarity_dictionary_norm[ij]) +
                                                       CF_similarity_shrink)

    print ("Combine CB and CF Similarities:")
    CB_similarity_num = {}
    CB_similarity_norm = {}
    CB_similarity_dict = {}
    for item in item_item_similarity_dictionary:
        CB_similarity_num[item] = {}
        similar_items = item_item_similarity_dictionary[item]
        att_i = items_attributes_dictionary[item]
        for item2 in similar_items:
            att_i2 = items_attributes_dictionary[item2]
            for attribute in att_i:
                if (att_i2.has_key(attribute)):
                    if (CB_similarity_num[item].has_key(item2)):
                        CB_similarity_num[item][item2] += items_attributes_dictionary[item][attribute] * \
                                                          items_attributes_dictionary[item2][attribute]
                    else:
                        CB_similarity_num[item][item2] = items_attributes_dictionary[item][attribute] * \
                                                         items_attributes_dictionary[item2][attribute]

    for item in CB_similarity_num:
        # For each attribute of the user
        for attribute in items_attributes_dictionary[item]:
            # Calculate the norm of the vector corresponding to the user attributes
            if (CB_similarity_norm.has_key(item)):
                CB_similarity_norm[item] += math.pow(items_attributes_dictionary[item][attribute], 2)
            else:
                CB_similarity_norm[item] = math.pow(items_attributes_dictionary[item][attribute], 2)
        CB_similarity_norm[item] = math.sqrt(CB_similarity_norm[item])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for item in CB_similarity_num:
        CB_similarity_dict[item] = {}
        # Calculate the user-user similarity
        for item_j in CB_similarity_num[item]:
            CB_similarity_dict[item][item_j] = CB_similarity_num[item][item_j] / (CB_similarity_norm[item] *
                                                                                  CB_similarity_norm[item_j] +
                                                                                  CB_similarity_shrink)

    print ("Similarities combination:")
    for item in item_item_similarity_dictionary:
        similar_items = item_item_similarity_dictionary[item]
        for item2 in similar_items:
            if (CB_similarity_dict[item].has_key(item2)):
                item_item_similarity_dictionary[item][item2] += (w * CB_similarity_dict[item][item2])

    if (KNN == 0):
        return item_item_similarity_dictionary
    else:
        item_item_KNN_similarity_dictionary = {}
        for item in item_item_similarity_dictionary:
            item_item_KNN_similarity_dictionary[item] = {}
            KNN_sim_items = sorted(item_item_similarity_dictionary[item].items(), key=operator.itemgetter(1))
            KNN_sim_items_desc = sorted(KNN_sim_items, key=lambda tup: -tup[1])
            for sim_item in KNN_sim_items_desc:
                if (len(item_item_KNN_similarity_dictionary[item]) < KNN):
                    item_item_KNN_similarity_dictionary[item][sim_item[0]] = item_item_similarity_dictionary[item][
                        sim_item[0]]

        return item_item_KNN_similarity_dictionary

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
                if (user in user_user_similarity_dictionary[user2]):
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

# Function to create the normalized recommendations for User_Based
def CFUserBasedPredictNormalizedRecommendation(target_users, user_user_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
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
                if (user in user_user_similarity_dictionary[user2]):
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

    print ("Ratings estimate and Normalization:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for user in users_prediction_dictionary_num:
        users_prediction_dictionary[user] = {}
        max_prediction = 0
        # For each item predicted for the user
        for item in users_prediction_dictionary_num[user]:
            # Evaluate the prediction of that item for that user
            if not (item in user_items_dictionary[user]):
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)
                    max_prediction = max(max_prediction, users_prediction_dictionary[user][item])

        for item in users_prediction_dictionary[user]:
            users_prediction_dictionary[user][item] = users_prediction_dictionary[user][item] / max_prediction

    return users_prediction_dictionary

# Function to create the recommendations for Item_Based
def CFItemBasedPredictRecommendation(target_users, item_item_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                     prediction_shrink, CF_IDF):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users['user_id']:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                ij_s_dict = item_item_similarity_dictionary[ij]
                # For each similar item in the dictionary
                for ii in ij_s_dict:
                    if (i_r_dict.has_key(ii)):
                        continue
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[uu].has_key(ii)):
                        users_prediction_dictionary_num[uu][ii] = CF_IDF[ij] * ij_s_dict[ii] #i_r_dict[ij] * ij_s_dict[ii]
                        users_prediction_dictionary_den[uu][ii] = ij_s_dict[ii]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[uu][ii] += CF_IDF[ij] * ij_s_dict[ii] #i_r_dict[ij] * ij_s_dict[ii]
                        users_prediction_dictionary_den[uu][ii] += ij_s_dict[ii]

    print ("Ratings estimate:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for uu in users_prediction_dictionary_num:
        users_prediction_dictionary[uu] = {}
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if (active_items_to_recommend.has_key(ii)):
                users_prediction_dictionary[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                      (users_prediction_dictionary_den[uu][ii] + prediction_shrink)

    return users_prediction_dictionary

# Function to create the normalized recommendations for Item_Based
def CFItemBasedPredictNormalizedRecommendation(target_users, item_item_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                               prediction_shrink, CF_IDF):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users['user_id']:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                ij_s_dict = item_item_similarity_dictionary[ij]
                # For each similar item in the dictionary
                for ii in ij_s_dict:
                    if (i_r_dict.has_key(ii)):
                        continue
                    # If the item was not predicted yet for the user, add it
                    if not (users_prediction_dictionary_num[uu].has_key(ii)):
                        users_prediction_dictionary_num[uu][ii] = CF_IDF[ij] * ij_s_dict[ii] #i_r_dict[ij] * ij_s_dict[ii]
                        users_prediction_dictionary_den[uu][ii] = ij_s_dict[ii]
                    # Else Evaluate its contribution
                    else:
                        users_prediction_dictionary_num[uu][ii] += CF_IDF[ij] * ij_s_dict[ii] #i_r_dict[ij] * ij_s_dict[ii]
                        users_prediction_dictionary_den[uu][ii] += ij_s_dict[ii]

    print ("Ratings estimate and Normalization:")
    # For each target user (users_prediction_dictionary_num contains all target users)
    for uu in users_prediction_dictionary_num:
        users_prediction_dictionary[uu] = {}
        max_prediction = 0
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if (active_items_to_recommend.has_key(ii)):
                users_prediction_dictionary[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                      (users_prediction_dictionary_den[uu][ii] + prediction_shrink)
                max_prediction = max(max_prediction, users_prediction_dictionary[uu][ii])

        for item in users_prediction_dictionary[uu]:
            users_prediction_dictionary[uu][item] = users_prediction_dictionary[uu][item] / max_prediction

    return users_prediction_dictionary

# Function to create the recommendations for Hybrid Weighted
def CFHybridWeightedPredictRecommendation(user_based_users_prediction, item_based_users_predictions, weight):
    print("Prediction for Hybrid Weighted Algorithm")
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
    print("Sorting predictions for Hybrid Ranked Algorithm")
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
    print("Combine predictions for Hybrid Ranked Algorithm")
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

# Function to create the recommendations for Hybrid Rank
def CFHybridRankPredictNormalizedRecommendation(user_based_users_prediction, item_based_users_predictions, user_based_weight,
                                                item_based_weight):
    users_prediction_dictionary = {}
    print("Combine predictions for Hybrid Ranked Algorithm")
    # for each user in the User based prediction
    for user in user_based_users_prediction:
        users_prediction_dictionary[user] = {}
        # for each item in the User based prediction
        for item in user_based_users_prediction[user]:
            users_prediction_dictionary[user][item] = user_based_weight * user_based_users_prediction[user][item]
    # for each user in the Item based prediction
    for user in item_based_users_predictions:
        for item in item_based_users_predictions[user]:
            if (users_prediction_dictionary[user].has_key(item)):
                users_prediction_dictionary[user][item] += item_based_weight * item_based_users_predictions[user][item]
            # else assign the value to the item
            else:
                users_prediction_dictionary[user][item] = item_based_weight * item_based_users_predictions[user][item]

    return users_prediction_dictionary

# Function to fill with Top Popular Items
def Top_Popular_Filling(users_prediction_dictionary, CF_IB_IDF):
    TopPopular_items = dict(sorted(CF_IB_IDF.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
    for user in users_prediction_dictionary:
        for top_pop in TopPopular_items:
            if (len(users_prediction_dictionary[user]) < 5):
                users_prediction_dictionary[user][top_pop] = 0

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