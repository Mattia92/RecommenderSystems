from __future__ import division
import math
import numpy
import operator
from collections import OrderedDict

#Function to initialize users_attributes and attributes_users dictionaries
def InitializeDictionaries_user(user_profile, user_cols):
    # Create the dictionary needed to compute the similarity between users
    # It is the User content matrix build with dictionaries
    # Dictionary is a list of elements, each element is defined as following
    # dict {user -> (list of {attribute -> value})}
    print ("Create users_attributes dictionary")
    users_attributes = {}
    # for each row of the user_profile csv
    for i, row in user_profile.iterrows():
        # initialize the dictionary of the user
        users_attributes[row['user']] = {}
        # for each attribute of the user
        for att in user_cols:
            if not (att == 'user'):
                # if the attribute is job_roles then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the field job_roles is 0 insert nothing
                if (att == 'job'):
                    if not (row[att] == '0'):
                        jobs = str(row[att]).split(",")
                        for j in jobs:
                            users_attributes[row['user']][att + '_' + str(j)] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'exp_years' or att == 'exp_years_current'):
                    if not (row[att] == 0 or math.isnan(row[att])):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the attribute is edu_field_of_studies then split the string obtaining the various fields and insert them in
                # the dictionary
                elif (att == 'edu_fiel'):
                    if type(row[att]) == str:
                        fields = str(row[att]).split(",")
                        for f in fields:
                            users_attributes[row['user']][att + '_' + str(f)] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    #continue
                    if type(row[att]) == str:
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    #continue
                    if (row['country'] == 'de'):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the attribute is edu_deg don't consider null value or 0
                elif (att == 'edu_deg'):
                    if not (math.isnan(row[att]) or row[att] == 0):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                # if the column type is int or float discard Null values
                elif (user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        users_attributes[row['user']][att + '_' + str(row[att])] = 1
                else:
                    users_attributes[row['user']][att + '_' + str(row[att])] = 1

    # Create the dictionary containing for each attribute the list of users which have it
    # Dictionary is a list of elements, each element is defined as following
    # dict {attribute -> (list of {user -> value})}
    print ("Create attributes_users dictionary")
    attributes_users = {}
    # for each row of the user_profile csv
    for i, row in user_profile.iterrows():
        # for each attribute of the user
        for att in user_cols:
            if not (att == 'user'):
                # if the attribute is job_roles then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the field job_roles is 0 insert nothing
                if (att == 'job'):
                    if not (row[att] == '0'):
                        jobs = str(row[att]).split(",")
                        for j in jobs:
                            # if the dictionary is not already initialized do it
                            if not attributes_users.has_key(att + '_' + str(j)):
                                attributes_users[att + '_' + str(j)] = {}
                            attributes_users[att + '_' + str(j)][row['user']] = 1
                # if the attribute is edu_field_of_studies then split the string obtaining the various fields and insert them in
                # the dictionary
                elif (att == 'edu_fiel'):
                    if type(row[att]) == str:
                        fields = str(row[att]).split(",")
                        for f in fields:
                            if not attributes_users.has_key(att + '_' + str(f)):
                                attributes_users[att + '_' + str(f)] = {}
                            attributes_users[att + '_' + str(f)][row['user']] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    #continue
                    if type(row[att]) == str:
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    #continue
                    if (row['country'] == 'de'):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'exp_years' or att == 'exp_years_current'):
                    if not (row[att] == 0 or math.isnan(row[att])):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the attribute is edu_deg don't consider null value or 0
                elif (att == 'edu_deg'):
                    if not (math.isnan(row[att]) or row[att] == 0):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                # if the column type is int or float discard Null values
                elif (user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        if not attributes_users.has_key(att + '_' + str(row[att])):
                            attributes_users[att + '_' + str(row[att])] = {}
                        attributes_users[att + '_' + str(row[att])][row['user']] = 1
                else:
                    if not attributes_users.has_key(att + '_' + str(row[att])):
                        attributes_users[att + '_' + str(row[att])] = {}
                    attributes_users[att + '_' + str(row[att])][row['user']] = 1

    return users_attributes, attributes_users

#Function to initialize users_attributes and attributes_users dictionaries
def InitializeDictionaries_item(item_profile, item_cols):
    # Create the dictionary needed to compute the similarity between items
    # It is the item content matrix build with dictionaries
    # Dictionary is a list of elements, each element is defined as following
    # dict {item -> (list of {attribute -> value})}
    print ("Create items_attributes dictionary")
    items_attributes = {}
    # for each row of the item_profile csv
    for i, row in item_profile.iterrows():
        # initialize the dictionary of the user
        items_attributes[row['item']] = {}
        # for each attribute of the item
        for att in item_cols:
            if not (att == 'item'):
                # if the attribute is title or tag then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the attribute is 0 insert nothing
                if (att == 'title' or att == 'tags'):
                    if not (row[att] == '0'):
                        titles = str(row[att]).split(",")
                        for t in titles:
                            items_attributes[row['item']][att + '_' + str(t)] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'employ'):
                    if not (row[att] == 0):
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    #continue
                    if type(row[att]) == str:
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1
                # only the item having country equal to de has this attribute
                elif (att == 'region'):
                    #continue
                    if (row['country'] == 'de'):
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1
                elif (att == 'created_at' or att == 'active_during_test'):
                    continue
                elif(att == 'latitude' or att == 'longitude'):
                    continue
                # if the column type is int or float discard Null values
                elif (item_profile[att].dtype == numpy.int64 or item_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        items_attributes[row['item']][att + '_' + str(row[att])] = 1

    # Create the dictionary containing for each attribute the list of users which have it
    # Dictionary is a list of elements, each element is defined as following
    # dict {attribute -> (list of {user -> value})}
    print ("Create attributes_items dictionary")
    attributes_items = {}
    # for each row of the user_profile csv
    for i, row in item_profile.iterrows():
        # for each attribute of the user
        for att in item_cols:
            if not (att == 'item'):
                # if the attribute is title or tag then split the string obtaining the various jobs and insert them in the dictionary
                # if the value of the attribute is 0 insert nothing
                if (att == 'title' or att == 'tags'):
                    if not (row[att] == '0'):
                        titles = str(row[att]).split(",")
                        for t in titles:
                            # if the dictionary is not already initialized do it
                            if not attributes_items.has_key(att + '_' + str(t)):
                                attributes_items[att + '_' + str(t)] = {}
                            attributes_items[att + '_' + str(t)][row['item']] = 1
                # if the attribute is one of the following consider them only if they are not equal to 0
                elif (att == 'career' or att == 'employ'):
                    if not (row[att] == 0):
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
                # if the attribute is country don't consider float values
                elif (att == 'country'):
                    #continue
                    if type(row[att]) == str:
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
                # only the user user having country equal to de has this attribute
                elif (att == 'region'):
                    #continue
                    if (row['country'] == 'de'):
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
                elif (att == 'created_at' or att == 'active_during_test'):
                    continue
                elif(att == 'latitude' or att == 'longitude'):
                    continue
                # if the column type is int or float discard Null values
                elif (item_profile[att].dtype == numpy.int64 or item_profile[att].dtype == numpy.float64):
                    if not (math.isnan(row[att])):
                        if not attributes_items.has_key(att + '_' + str(row[att])):
                            attributes_items[att + '_' + str(row[att])] = {}
                        attributes_items[att + '_' + str(row[att])][row['item']] = 1
    return items_attributes, attributes_items

# Function to compute TF and IDF
def ComputeTF_IDF(user_attributes, attribute_users):
    # create the tf(time frequency) dictionary for each user
    # each attribute of the same user has the same tf value
    users_tf = {}
    for user in user_attributes:#.keys():
        users_tf[user] = 1 / len(user_attributes[user])
    # create the idf dictionary for each attribute
    attributes_idf = {}
    n_users = len(user_attributes.keys())
    for attribute in attribute_users:#.keys():
        attributes_idf[attribute] = math.log10(n_users / len(attribute_users[attribute]))
    # modify each attribute value including tf-idf
    for user in user_attributes:#.keys():
        for attribute in user_attributes[user]:#.keys():
            user_attributes[user][attribute] *= users_tf[user] * attributes_idf[attribute]
            attribute_users[attribute][user] *= users_tf[user] * attributes_idf[attribute]
    # sort the dictionary by attribute values
    for attribute in attribute_users:#.keys():
        attribute_users[attribute] = OrderedDict(
            sorted(attribute_users[attribute].items(), key=lambda t: -t[1]))
    for user in user_attributes:
        user_attributes[user] = OrderedDict(
            sorted(user_attributes[user].items(), key=lambda t: -t[1]))

    return user_attributes, attribute_users

# Function to compute TF and IDF
def ComputeTF_IDF_CB_UB(user_attributes, attribute_users, target_users, user_at_least_one_interaction, KNN):
    # create the tf(time frequency) dictionary for each user
    # each attribute of the same user has the same tf value
    users_tf = {}
    for user in user_attributes:
        users_tf[user] = 1 / len(user_attributes[user])
    # create the idf dictionary for each attribute
    attributes_idf = {}
    n_users = len(user_attributes.keys())
    for attribute in attribute_users:
        attributes_idf[attribute] = math.log10(n_users / len(attribute_users[attribute]))
    # modify each attribute value including tf-idf
    for user in user_attributes:
        for attribute in user_attributes[user]:
            user_attributes[user][attribute] *= users_tf[user] * attributes_idf[attribute]
            attribute_users[attribute][user] *= users_tf[user] * attributes_idf[attribute]
    # create the dictionary of target users with their KNN attributes
    user_KNN_attributes = {}
    for user in target_users:
        user_KNN_attributes[user] = {}
        user_attributes[user] = OrderedDict(
            sorted(user_attributes[user].items(), key=lambda t: -t[1]))
        KNN_attributes = user_attributes[user].keys()
        for attribute in KNN_attributes[:KNN]:
            user_KNN_attributes[user][attribute] = user_attributes[user][attribute]
    user_one_interaction_KNN_attributes = {}
    for user in user_at_least_one_interaction:
        user_one_interaction_KNN_attributes[user] = {}
        user_attributes[user] = OrderedDict(
            sorted(user_attributes[user].items(), key=lambda t: -t[1]))
        KNN_attributes = user_attributes[user].keys()
        for attribute in KNN_attributes[:KNN]:
            user_one_interaction_KNN_attributes[user][attribute] = user_attributes[user][attribute]

    attribute_KNN_users = {}
    for user in user_one_interaction_KNN_attributes:
        for attribute in user_one_interaction_KNN_attributes[user]:
            if (attribute_KNN_users.has_key(attribute)):
                attribute_KNN_users[attribute][user] = user_one_interaction_KNN_attributes[user][attribute]
            else:
                attribute_KNN_users[attribute] = {}
                attribute_KNN_users[attribute][user] = user_one_interaction_KNN_attributes[user][attribute]

    return user_KNN_attributes, attribute_KNN_users, user_one_interaction_KNN_attributes

# Function to compute TF and IDF
def ComputeTF_IDF_CB_IB(item_attributes, attribute_items, active_items, item_at_least_one_interaction_by_target_users, KNN):
    # create the tf(time frequency) dictionary for each user
    # each attribute of the same user has the same tf value
    items_tf = {}
    for item in item_attributes:
        items_tf[item] = 1 / len(item_attributes[item])
    # create the idf dictionary for each attribute
    attributes_idf = {}
    n_items = len(item_attributes.keys())
    for attribute in attribute_items:
        attributes_idf[attribute] = math.log10(n_items / len(attribute_items[attribute]))
    # modify each attribute value including tf-idf
    for item in item_attributes:
        for attribute in item_attributes[item]:
            item_attributes[item][attribute] *= items_tf[item] * attributes_idf[attribute]
    # create the dictionary of target users with their KNN attributes
    item_KNN_attributes = {}
    for item in active_items:
        item_KNN_attributes[item] = {}
        item_attributes[item] = OrderedDict(
            sorted(item_attributes[item].items(), key=lambda t: -t[1]))
        KNN_attributes = item_attributes[item].keys()
        for attribute in KNN_attributes[:KNN]:
            item_KNN_attributes[item][attribute] = item_attributes[item][attribute]
    item_interacted_by_target_users_KNN_attributes = {}
    for item in item_at_least_one_interaction_by_target_users:
        item_interacted_by_target_users_KNN_attributes[item] = {}
        item_attributes[item] = OrderedDict(
            sorted(item_attributes[item].items(), key=lambda t: -t[1]))
        KNN_attributes = item_attributes[item].keys()
        for attribute in KNN_attributes[:KNN]:
            item_interacted_by_target_users_KNN_attributes[item][attribute] = item_attributes[item][attribute]

    attribute_KNN_items = {}
    for item in item_interacted_by_target_users_KNN_attributes:
        for attribute in item_interacted_by_target_users_KNN_attributes[item]:
            if (attribute_KNN_items.has_key(attribute)):
                attribute_KNN_items[attribute][item] = item_interacted_by_target_users_KNN_attributes[item][attribute]
            else:
                attribute_KNN_items[attribute] = {}
                attribute_KNN_items[attribute][item] = item_interacted_by_target_users_KNN_attributes[item][attribute]
    # attribute_KNN_items dict sorted by items
    for attribute in attribute_KNN_items:
        attribute_KNN_items[attribute] = OrderedDict(
            sorted(attribute_KNN_items[attribute].items(), key=lambda t: -t[1]))

    return item_KNN_attributes, attribute_KNN_items, item_interacted_by_target_users_KNN_attributes

# Function to build the User-User Similarity Dictionary
def CBUserUserSimilarity(target_users_dictionary, user_at_least_one_interaction, user_attributes_dictionary,
                         attributes_users_dictionary, similarity_shrink, KNN):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    #user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_similarity_dictionary_norm = {}

    print ("Create dictionaries for CB user-user similarity")
    # For each user in the dictionary
    i = 1
    size = len(target_users_dictionary)
    for user in target_users_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        # Calculate the similarity only for the target users
        user_att = user_attributes_dictionary[user] #dictionary of all the attributes of the user
        user_user_similarity_dictionary_num[user] = {}
        # For each attribute of the user
        for att in user_att:
            user_list = attributes_users_dictionary[att].keys() #list of users that has this attribute
            for u in user_list[:2500]:
                # Don't consider the similarity between the same users
                if u == user:
                    continue
                else:
                    if (user_at_least_one_interaction.has_key(u)):
                        # Create the dictionary containing the numerator of the similarity
                        if(user_user_similarity_dictionary_num[user].has_key(u)):
                            user_user_similarity_dictionary_num[user][u] += user_attributes_dictionary[user][att] *\
                                                                            user_attributes_dictionary[u][att]
                        else:
                            user_user_similarity_dictionary_num[user][u] = user_attributes_dictionary[user][att] *\
                                                                            user_attributes_dictionary[u][att]
    # For each user in the dictionary
    for user in user_attributes_dictionary:
        # For each attribute of the user
        for attribute in user_attributes_dictionary[user]:
            # Calculate the norm of the vector corresponding to the user attributes
            if (user_similarity_dictionary_norm.has_key(user)):
                user_similarity_dictionary_norm[user] += math.pow(user_attributes_dictionary[user][attribute], 2)
            else:
                user_similarity_dictionary_norm[user] = math.pow(user_attributes_dictionary[user][attribute], 2)
        user_similarity_dictionary_norm[user] = math.sqrt(user_similarity_dictionary_norm[user])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for user in user_user_similarity_dictionary_num:
        #user_user_similarity_dictionary[user] = {}
        # Calculate the user-user similarity
        for user_j in user_user_similarity_dictionary_num[user]:
            user_user_similarity_dictionary_num[user][user_j] = user_user_similarity_dictionary_num[user][user_j] / \
                                                            (user_similarity_dictionary_norm[user] *
                                                             user_similarity_dictionary_norm[user_j] + similarity_shrink)

    if (KNN == 0):
        return user_user_similarity_dictionary_num
    else:
        user_user_KNN_similarity_dictionary = {}
        for user in user_user_similarity_dictionary_num:
            user_user_KNN_similarity_dictionary[user] = {}
            KNN_sim_users = sorted(user_user_similarity_dictionary_num[user].items(), key=operator.itemgetter(1))
            KNN_sim_users_desc = sorted(KNN_sim_users, key=lambda tup: -tup[1])
            for sim_user in KNN_sim_users_desc:
                if (len(user_user_KNN_similarity_dictionary[user]) < KNN):
                    user_user_KNN_similarity_dictionary[user][sim_user[0]] = user_user_similarity_dictionary_num[user][sim_user[0]]
        return user_user_KNN_similarity_dictionary

# Function to build the User-User Similarity Dictionary
def CBUserUserSimilarityKNNAttributes(user_attributes_dictionary, attributes_users_dictionary, user_one_interact_attributes_dictionary,
                                      similarity_shrink, KNN):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    #user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_similarity_dictionary_norm = {}

    print ("Create dictionaries for CB user-user similarity")
    # For each user in the dictionary
    i = 1
    size = len(user_attributes_dictionary)
    for user in user_attributes_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        # Calculate the similarity only for the target users
        user_att = user_attributes_dictionary[user] #dictionary of all the attributes of the user
        user_user_similarity_dictionary_num[user] = {}
        # For each attribute of the user
        for att in user_att:
            if (attributes_users_dictionary.has_key(att)):
                user_list = attributes_users_dictionary[att] #list of users that has this attribute
                for u in user_list:
                    # Don't consider the similarity between the same users
                    if u == user:
                        continue
                    else:
                        # Create the dictionary containing the numerator of the similarity
                        if(user_user_similarity_dictionary_num[user].has_key(u)):
                            user_user_similarity_dictionary_num[user][u] += user_attributes_dictionary[user][att] *\
                                                                            attributes_users_dictionary[att][u]
                        else:
                            user_user_similarity_dictionary_num[user][u] = user_attributes_dictionary[user][att] * \
                                                                           attributes_users_dictionary[att][u]
    # For each user in the dictionary
    for user in user_attributes_dictionary:
        # For each attribute of the user
        for attribute in user_attributes_dictionary[user]:
            # Calculate the norm of the vector corresponding to the user attributes
            if (user_similarity_dictionary_norm.has_key(user)):
                user_similarity_dictionary_norm[user] += math.pow(user_attributes_dictionary[user][attribute], 2)
            else:
                user_similarity_dictionary_norm[user] = math.pow(user_attributes_dictionary[user][attribute], 2)
        user_similarity_dictionary_norm[user] = math.sqrt(user_similarity_dictionary_norm[user])
    for user in user_one_interact_attributes_dictionary:
        if not(user_similarity_dictionary_norm.has_key(user)):
            for attribute in user_one_interact_attributes_dictionary[user]:
                if (user_similarity_dictionary_norm.has_key(user)):
                    user_similarity_dictionary_norm[user] += math.pow(user_one_interact_attributes_dictionary[user][attribute], 2)
                else:
                    user_similarity_dictionary_norm[user] = math.pow(user_one_interact_attributes_dictionary[user][attribute], 2)
            user_similarity_dictionary_norm[user] = math.sqrt(user_similarity_dictionary_norm[user])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for user in user_user_similarity_dictionary_num:
        # Calculate the user-user similarity
        for user_j in user_user_similarity_dictionary_num[user]:
            user_user_similarity_dictionary_num[user][user_j] = user_user_similarity_dictionary_num[user][user_j] / \
                                                            (user_similarity_dictionary_norm[user] *
                                                             user_similarity_dictionary_norm[user_j] + similarity_shrink)

    if (KNN == 0):
        return user_user_similarity_dictionary_num
    else:
        user_user_KNN_similarity_dictionary = {}
        for user in user_user_similarity_dictionary_num:
            user_user_KNN_similarity_dictionary[user] = {}
            KNN_sim_users = sorted(user_user_similarity_dictionary_num[user].items(), key=operator.itemgetter(1))
            KNN_sim_users_desc = sorted(KNN_sim_users, key=lambda tup: -tup[1])
            for sim_user in KNN_sim_users_desc:
                if (len(user_user_KNN_similarity_dictionary[user]) < KNN):
                    user_user_KNN_similarity_dictionary[user][sim_user[0]] = user_user_similarity_dictionary_num[user][sim_user[0]]
        return user_user_KNN_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CBItemItemSimilarity(item_at_least_one_interaction, active_items_dictionary, item_attribute_dictionary,
                         attribute_items_dictionary):
    item_item_similarity_dictionary_num = {}

    print ("Create dictionaries for CB item-item similarity")

    i = 1
    size = len(item_at_least_one_interaction)
    for item in item_at_least_one_interaction:
        print (str(i) + "/" + str(size))
        i = i + 1
        item_att = item_attribute_dictionary[item].keys()
        item_item_similarity_dictionary_num[item] = {}
        for att in item_att[:5]:
            item_list = attribute_items_dictionary[att]
            for ij in item_list:
                if ij == item:
                    continue
                else:
                    if (active_items_dictionary.has_key(ij)):
                        if (item_item_similarity_dictionary_num[item].has_key(ij)):
                            item_item_similarity_dictionary_num[item][ij] += item_attribute_dictionary[item][att] * \
                                                                             item_attribute_dictionary[ij][att]
                        else:
                            item_item_similarity_dictionary_num[item][ij] = item_attribute_dictionary[item][att] * \
                                                                            item_attribute_dictionary[ij][att]

    return item_item_similarity_dictionary_num

def CBItemItemSimilarityEstimate(item_item_similarity_dictionary, item_attribute_dictionary, similarity_shrink, KNN):
    item_similarity_dictionary_norm = {}
    for item in item_attribute_dictionary:
        for attribute in item_attribute_dictionary[item]:
            if (item_similarity_dictionary_norm.has_key(item)):
                item_similarity_dictionary_norm[item] += math.pow(item_attribute_dictionary[item][attribute], 2)
            else:
                item_similarity_dictionary_norm[item] = math.pow(item_attribute_dictionary[item][attribute], 2)
        item_similarity_dictionary_norm[item] = math.sqrt(item_similarity_dictionary_norm[item])

    print ("Similarities estimate:")
    i = 1
    size = len(item_item_similarity_dictionary)
    for item in item_item_similarity_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        for item_j in item_item_similarity_dictionary[item]:
            item_item_similarity_dictionary[item][item_j] = item_item_similarity_dictionary[item][item_j] / \
                                                            (item_similarity_dictionary_norm[item] *
                                                             item_similarity_dictionary_norm[item_j] + similarity_shrink)

    print ("Similarity KNN")
    if (KNN == 0):
        return item_item_similarity_dictionary
    else:
        i = 1
        item_item_KNN_similarity_dictionary = {}
        for item in item_item_similarity_dictionary:
            print (str(i) + "/" + str(size))
            i = i + 1
            item_item_KNN_similarity_dictionary[item] = {}
            KNN_sim_items = sorted(item_item_similarity_dictionary[item].items(), key=operator.itemgetter(1))
            KNN_sim_items_desc = sorted(KNN_sim_items, key=lambda tup: -tup[1])
            for sim_item in KNN_sim_items_desc:
                if (len(item_item_KNN_similarity_dictionary[item]) < KNN):
                    item_item_KNN_similarity_dictionary[item][sim_item[0]] = item_item_similarity_dictionary[item][sim_item[0]]
        return item_item_KNN_similarity_dictionary

# Function to build the Item-Item Similarity Dictionary
def CBItemItemSimilarityKNNAttributes(item_attribute_dictionary, attribute_items_dictionary):

    item_item_similarity_dictionary_num = {}
    print ("Create dictionaries for CB item-item similarity")
    i = 1
    size = len(item_attribute_dictionary)
    for item in item_attribute_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        item_att = item_attribute_dictionary[item]
        item_item_similarity_dictionary_num[item] = {}
        for att in item_att:
            if (attribute_items_dictionary.has_key(att)):
                item_list = attribute_items_dictionary[att].keys()
                for ij in item_list[:500]:
                    if ij == item:
                        continue
                    else:
                        if(item_item_similarity_dictionary_num[item].has_key(ij)):
                            item_item_similarity_dictionary_num[item][ij] += item_attribute_dictionary[item][att] * \
                                                                             attribute_items_dictionary[att][ij]
                        else:
                            item_item_similarity_dictionary_num[item][ij] = item_attribute_dictionary[item][att] * \
                                                                            attribute_items_dictionary[att][ij]

    return item_item_similarity_dictionary_num

def CBItemItemSimilarityEstimateKNNAttributes(item_item_similarity_dictionary, item_attribute_dictionary, item_interacted_by_target_users_KNN_attributes,
                                              similarity_shrink, KNN):
    item_similarity_dictionary_norm = {}
    for item in item_attribute_dictionary:
        for attribute in item_attribute_dictionary[item]:
            if (item_similarity_dictionary_norm.has_key(item)):
                item_similarity_dictionary_norm[item] += math.pow(item_attribute_dictionary[item][attribute], 2)
            else:
                item_similarity_dictionary_norm[item] = math.pow(item_attribute_dictionary[item][attribute], 2)
        item_similarity_dictionary_norm[item] = math.sqrt(item_similarity_dictionary_norm[item])
    for item in item_interacted_by_target_users_KNN_attributes:
        if not(item_similarity_dictionary_norm.has_key(item)):
            for attribute in item_interacted_by_target_users_KNN_attributes[item]:
                if (item_similarity_dictionary_norm.has_key(item)):
                    item_similarity_dictionary_norm[item] += math.pow(item_interacted_by_target_users_KNN_attributes[item][attribute], 2)
                else:
                    item_similarity_dictionary_norm[item] = math.pow(item_interacted_by_target_users_KNN_attributes[item][attribute], 2)
            item_similarity_dictionary_norm[item] = math.sqrt(item_similarity_dictionary_norm[item])

    print ("Similarities estimate:")
    i = 1
    size = len(item_item_similarity_dictionary)
    for item in item_item_similarity_dictionary:
        print (str(i) + "/" + str(size))
        i = i + 1
        for item_j in item_item_similarity_dictionary[item]:
            item_item_similarity_dictionary[item][item_j] = item_item_similarity_dictionary[item][item_j] / \
                                                            (item_similarity_dictionary_norm[item] *
                                                             item_similarity_dictionary_norm[item_j] + similarity_shrink)

    # Change the dictionary from {active_item --> {item_interact_by_target_u --> score}}
    # to {item_interact_by_target_u --> {active_item --> score}}
    print ("Similarity KNN")
    item_item_KNN_similarity_dictionary = {}
    item_item_KNN_similarity_dictionary2 = {}
    if (KNN == 0):
        for item in item_item_similarity_dictionary:
            for itemsim in item_item_similarity_dictionary[item]:
                if (item_item_KNN_similarity_dictionary.has_key(itemsim)):
                    item_item_KNN_similarity_dictionary[itemsim][item] = item_item_similarity_dictionary[item][itemsim]
                else:
                    item_item_KNN_similarity_dictionary[itemsim] = {}
                    item_item_KNN_similarity_dictionary[itemsim][item] = item_item_similarity_dictionary[item][itemsim]

        return item_item_KNN_similarity_dictionary
    else:
        i = 1
        for item in item_item_similarity_dictionary:
            print (str(i) + "/" + str(size))
            i = i + 1
            item_item_KNN_similarity_dictionary[item] = {}
            KNN_sim_items = sorted(item_item_similarity_dictionary[item].items(), key=operator.itemgetter(1))
            KNN_sim_items_desc = sorted(KNN_sim_items, key=lambda tup: -tup[1])
            for sim_item in KNN_sim_items_desc:
                if (len(item_item_KNN_similarity_dictionary[item]) < KNN):
                    item_item_KNN_similarity_dictionary[item][sim_item[0]] = item_item_similarity_dictionary[item][sim_item[0]]
        for item in item_item_KNN_similarity_dictionary:
            for itemsim in item_item_KNN_similarity_dictionary[item]:
                if (item_item_KNN_similarity_dictionary2.has_key(itemsim)):
                    item_item_KNN_similarity_dictionary2[itemsim][item] = item_item_similarity_dictionary[item][itemsim]
                else:
                    item_item_KNN_similarity_dictionary2[itemsim] = {}
                    item_item_KNN_similarity_dictionary2[itemsim][item] = item_item_similarity_dictionary[item][itemsim]

        return item_item_KNN_similarity_dictionary2

# Function to create the recommendations for User_Based
def CBUserBasedPredictRecommendation(target_users_dictionary, user_user_similarity_dictionary, user_items_dictionary, active_items_to_recommend,
                                     prediction_shrink):
    print ("Create dictionaries for CB User Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users_dictionary:
        users_prediction_dictionary_num[user] = {}
        # Get dictionary of similar users and the value of similarity
        uus_list = user_user_similarity_dictionary[user]
        # For each similar user in the dictionary
        for user2 in uus_list:
            #if(user_items_dictionary.has_key(user2)):
            # Get the dictionary of items with which this user has interact
            u2_item_list = user_items_dictionary[user2]
            #if (user in user_user_similarity_dictionary[user2]):
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
            if (user_items_dictionary.has_key(user)):
                if not (item in user_items_dictionary[user]):
                    if (active_items_to_recommend.has_key(item)):
                        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                                (users_prediction_dictionary_norm[user] + prediction_shrink)
            else:
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)

    return users_prediction_dictionary

# Function to create the normalized recommendations for User_Based
def CBUserBasedPredictNormalizedRecommendation(target_users_dictionary, user_user_similarity_dictionary, user_items_dictionary,
                                               recent_items_dictionary, active_items_to_recommend, prediction_shrink):
    print ("Create dictionaries for CB User Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_norm = {}
    # For each target user
    for user in target_users_dictionary:
        users_prediction_dictionary_num[user] = {}
        # Get dictionary of similar users and the value of similarity
        uus_list = user_user_similarity_dictionary[user]
        # For each similar user in the dictionary
        for user2 in uus_list:
            if (user_items_dictionary.has_key(user2)):
                # Get the dictionary of items with which this user has interact
                u2_item_list = user_items_dictionary[user2]
                # if (user in user_user_similarity_dictionary[user2]):
                # For each item in the dictionary
                for i in u2_item_list:
                    if (recent_items_dictionary.has_key(i)):
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
            if (user_items_dictionary.has_key(user)):
                if not (item in user_items_dictionary[user]):
                    if (active_items_to_recommend.has_key(item)):
                        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                                  (users_prediction_dictionary_norm[user] + prediction_shrink)
                        max_prediction = max(max_prediction, users_prediction_dictionary[user][item])
            else:
                if (active_items_to_recommend.has_key(item)):
                    users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                              (users_prediction_dictionary_norm[user] + prediction_shrink)
                    max_prediction = max(max_prediction, users_prediction_dictionary[user][item])

        # for item in users_prediction_dictionary[user]:
        #     rank = users_prediction_dictionary[user][item] / max_prediction
        #     pop = item_number_click_dictionary[item] / max_n_click
        #     users_prediction_dictionary[user][item] = rank * (1.5 + pop)

        for item in users_prediction_dictionary[user]:
            users_prediction_dictionary[user][item] = users_prediction_dictionary[user][item] / max_prediction

    return users_prediction_dictionary

# Function to create the recommendations for Item_Based
def CBItemBasedPredictRecommendation(active_items_dictionary, item_item_similarity_dictionary, user_items_dictionary, target_users_dictionary,
                                     prediction_shrink, CF_IDF):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    #users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users_dictionary:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                #if (ij in active_items_dictionary):
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
        #users_prediction_dictionary[uu] = {}
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if (active_items_dictionary.has_key(ii)):
                users_prediction_dictionary_num[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                      (users_prediction_dictionary_den[uu][ii] + prediction_shrink)

    return users_prediction_dictionary_num

# Function to create the recommendations for Item_Based
def CBItemBasedPredictNormalizedRecommendation(active_items_dictionary, item_item_similarity_dictionary, user_items_dictionary,
                                               recent_items_dictionary, target_users_dictionary, prediction_shrink, CF_IDF):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    #users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users_dictionary:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                #if (ij in active_items_dictionary):
                ij_s_dict = item_item_similarity_dictionary[ij]
                # For each similar item in the dictionary
                for ii in ij_s_dict:
                    if (i_r_dict.has_key(ii)):
                        continue
                    if (recent_items_dictionary.has_key(ii)):
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
        max_prediction = 0
        #users_prediction_dictionary[uu] = {}
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if not (ii in user_items_dictionary):
                if (active_items_dictionary.has_key(ii)):
                    users_prediction_dictionary_num[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                          (users_prediction_dictionary_den[uu][ii] + prediction_shrink)
                    max_prediction = max(max_prediction, users_prediction_dictionary_num[uu][ii])

        # for item in users_prediction_dictionary_num[uu]:
        #     rank = users_prediction_dictionary_num[uu][item] / max_prediction
        #     pop = item_number_click_dictionary[item] / max_n_click
        #     users_prediction_dictionary_num[uu][item] = rank * (1.5 + pop)

        for item in users_prediction_dictionary_num[uu]:
            users_prediction_dictionary_num[uu][item] = users_prediction_dictionary_num[uu][item] / max_prediction

    return users_prediction_dictionary_num

# Function to create the recommendations for Item_Based
def CBItemKNNAttributesBasedPredictNormalizedRecommendation(active_items_dictionary, item_item_similarity_dictionary, user_items_dictionary,
                                                            recent_items_dictionary, target_users_dictionary, prediction_shrink, CF_IDF):
    print ("Create dictionaries for CF Item Based user predictions")
    # Create the dictionary for users prediction
    # dict {user -> (list of {item -> prediction})}
    #users_prediction_dictionary = {}
    users_prediction_dictionary_num = {}
    users_prediction_dictionary_den = {}
    # For each target user
    for uu in target_users_dictionary:
        users_prediction_dictionary_num[uu] = {}
        users_prediction_dictionary_den[uu] = {}
        # If user has interact with at least one item
        if (user_items_dictionary.has_key(uu)):
            # Get dictionary of items with which the user has interact
            i_r_dict = user_items_dictionary[uu]
            # For each item in this dictionary
            for ij in i_r_dict:
                # Get the dictionary of similar items and the value of similarity
                if (item_item_similarity_dictionary.has_key(ij)):
                    ij_s_dict = item_item_similarity_dictionary[ij]
                    # For each similar item in the dictionary
                    for ii in ij_s_dict:
                        if (i_r_dict.has_key(ii)):
                            continue
                        if (recent_items_dictionary.has_key(ii)):
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
        max_prediction = 0
        #users_prediction_dictionary[uu] = {}
        # For each item predicted for the user
        for ii in users_prediction_dictionary_num[uu]:
            # Evaluate the prediction of that item for that user
            if not (ii in user_items_dictionary[uu]):
                if (active_items_dictionary.has_key(ii)):
                    users_prediction_dictionary_num[uu][ii] = users_prediction_dictionary_num[uu][ii] / \
                                                          (users_prediction_dictionary_den[uu][ii] + prediction_shrink)
                    max_prediction = max(max_prediction, users_prediction_dictionary_num[uu][ii])

        #for item in users_prediction_dictionary_num[uu]:
        #    rank = users_prediction_dictionary_num[uu][item] / max_prediction
        #    pop = item_number_click_dictionary[item] / max_n_click
        #    users_prediction_dictionary_num[uu][item] = rank * (1.5 + pop)

        for item in users_prediction_dictionary_num[uu]:
            users_prediction_dictionary_num[uu][item] = users_prediction_dictionary_num[uu][item] / max_prediction

    return users_prediction_dictionary_num

def CBWritePredictions(output_filename, users_prediction_dictionary):
    print ("Writing predictions on " + output_filename)
    out_file = open(output_filename, "w")
    for user in users_prediction_dictionary:
        for item in users_prediction_dictionary[user]:
            out_file.write(str(user) + "\t" + str(item) + "\t" + str(users_prediction_dictionary[user][item]) + "\n")
    out_file.close()

def CBWrite_Top_Predictions(output_filename, users_prediction_dictionary):
    print ("Writing predictions on " + output_filename)
    out_file = open(output_filename, "w")
    for user in users_prediction_dictionary:
        users_prediction_dictionary[user] = OrderedDict(
            sorted(users_prediction_dictionary[user].items(), key=lambda t: -t[1]))
        items_predicted = users_prediction_dictionary[user].keys()
        for item in items_predicted[:300]:
            out_file.write(str(user) + "\t" + str(item) + "\t" + str(users_prediction_dictionary[user][item]) + "\n")
    out_file.close()

#Function to Read the predictions files
def CBRead_Predictions(output_filename):
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
def CBWriteResult(output_filename, users_prediction_dictionary):
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