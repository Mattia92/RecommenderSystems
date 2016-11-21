# Function to build the Item-Item Similarity Dictionary
# TODO: fix this function
def CFItemItemSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    item_item_similarity_dictionary = {}
    print ("Create dictionaries for item-item similarity")
    # For each item in the dictionary
    for item in item_users_dictionary:
        # Get the dictionary pointed by the item, containing the users which has interact with that item
        interacting_users = item_users_dictionary[item]
        # For each user in the dictionary pointed by the item
        for user in interacting_users:
            # Get the dictionary pointed by the user, containing the items with which the user has interact
            interacted_items = user_items_dictionary[user]
            # Get list of items with which this user has interact
            item_list = interacted_items.keys()
            # Instantiate the similarity dictionary
            # dict {item -> (dict2)}
            # dict2 will be {similar_item -> similarity}
            item_item_similarity_dictionary[item] = {}
            # For each item in the list of items
            for list_element in item_list:
                # If similar_item is already in dict2 create the sum of product of ratings
                if (item_item_similarity_dictionary[item].has_key(list_element)):
                    item_item_similarity_dictionary[item][list_element] += 1
                # Else the similar_item is added to dict2 and the product of ratings is set to 1
                else:
                    item_item_similarity_dictionary[item][list_element] = 1
        # Remove from similar_items the item itself
        if (item_item_similarity_dictionary[item].has_key(item)):
            del item_item_similarity_dictionary[item][item]
        # Evaluate the value of similarity
        for sim in item_item_similarity_dictionary[item]:
            item_item_similarity_dictionary[item][sim] /= ((math.sqrt(len(interacting_users)) *
                                                            math.sqrt(len(item_users_dictionary[sim]))) +
                                                           similarity_shrink)

    return item_item_similarity_dictionary

# For each target user
for user in target_users['user_id']:
    users_prediction_dictionary_num[user] = {}
    users_prediction_dictionary_den[user] = {}
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
                    users_prediction_dictionary_num[user][item2] = iis_list[item2] * 1  # i_list[item]
                    users_prediction_dictionary_den[user][item2] = iis_list[item2]
                # Else Evaluate its contribution
                else:
                    users_prediction_dictionary_num[user][item2] += iis_list[item2] * 1  # i_list[item]
                    users_prediction_dictionary_den[user][item2] += iis_list[item2]

print ("Ratings estimate:")
# For each target user (users_prediction_dictionary_num contains all target users)
for user in users_prediction_dictionary_num:
    users_prediction_dictionary[user] = {}
    # For each item predicted for the user
    for item in users_prediction_dictionary_num[user]:
        # Evaluate the prediction of that item for that user
        users_prediction_dictionary[user][item] = users_prediction_dictionary_num[user][item] / \
                                                  (users_prediction_dictionary_den[user][item] + prediction_shrink)