from __future__ import division
import math
import numpy as np

# Function to build the User-User Similarity Dictionary
def CBUserUserSimilarity(target_users, user_attributes_dictionary, attributes_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_user_similarity_dictionary_den1 = {}
    user_user_similarity_dictionary_den2 = {}
    user_similarity_dictionary_norm = {}

    print ("Create dictionaries for CB user-user similarity")
    # For each user in the dictionary
    for user in user_attributes_dictionary:
        # Calculate the similarity only for the target users
        if user in target_users['user_id'].unique():
            user_att = user_attributes_dictionary[user] #dictionary of all the attributes of the user
            user_user_similarity_dictionary_num[user] = {}
            # For eachattribute of the user
            for att in user_att:
                user_list = attributes_users_dictionary[att].keys() #list of users that has this attribute
                # for first 10 users
                for u in user_list[:10]:
                    # Don't consider the similarity between the same users
                    if u == user:
                        continue
                    else:
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
                user_similarity_dictionary_norm[user] += math.exp(user_attributes_dictionary[user][attribute])
            else:
                user_similarity_dictionary_norm[user] = math.exp(user_attributes_dictionary[user][attribute])
        user_similarity_dictionary_norm[user] = math.sqrt(user_similarity_dictionary_norm[user])

    print ("Similarities estimate:")
    # For each user in the dictionary
    for user in user_user_similarity_dictionary_num:
        user_user_similarity_dictionary[user] = {}
        # Calculate the user-user similarity
        for user_j in user_user_similarity_dictionary_num[user]:
            user_user_similarity_dictionary[user][user_j] = user_user_similarity_dictionary_num[user][user_j] / \
                                                            (user_similarity_dictionary_norm[user] * \
                                                             user_similarity_dictionary_norm[user_j] + similarity_shrink)

    return user_user_similarity_dictionary