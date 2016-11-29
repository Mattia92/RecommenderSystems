import pandas as pd
import CFAlgorithms
import CBAlgorithms

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by=['user_id', 'create_at'], ascending=[True, False])
interactions = interactions.drop('create_at', axis=1)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]
# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state


items = pd.read_csv('DataSet/user_profile.csv', sep='\t', header=0)

target_users = pd.read_csv('DataSet/target_users.csv')

print ("Create training and test Datasets")
test_dictionary = {}
i = 1
for index, row in interactions.iterrows():
    if not(test_dictionary.has_key(row['user_id'])):
        test_dictionary[row['user_id']] = []
        test_dictionary[row['user_id']].append(row['item_id'])
        interactions.drop(interactions.index[index])
    else:
        if (len(test_dictionary[row['user_id']]) < 6):
            test_dictionary[row['user_id']].append(row['item_id'])
            interactions.drop(interactions.index[index])

    print (str(i))
    i = i+1

interactions.to_csv("TestDataSet/training.csv", sep='\t', index=False)