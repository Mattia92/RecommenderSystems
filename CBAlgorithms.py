# Function to build the User-User Similarity Dictionary
def CBUserUserSimilarity(user_items_dictionary, item_users_dictionary, similarity_shrink):
    # Create the dictionary for the user_user similarity
    # dict {user -> (list of {user -> similarity})}
    user_user_similarity_dictionary = {}
    user_user_similarity_dictionary_num = {}
    user_user_similarity_dictionary_den1 = {}
    user_user_similarity_dictionary_den2 = {}
    print ("Create dictionaries for CB user-user similarity")