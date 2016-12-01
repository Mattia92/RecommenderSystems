import pandas as pd
import itertools as it
import CFAlgorithms
import CBAlgorithms
from collections import OrderedDict

# Importing all the files needed
cols = ['user_id', 'item_id', 'interaction', 'create_at']
interactions = pd.read_csv('DataSet/interactions.csv', sep='\t', names=cols, header=0)
# Sort interactions by time of creation in ascending order
# This is done because in dictionary when duplicate keys encountered during assignment, the last assignment wins
interactions = interactions.sort_values(by=['user_id', 'create_at'], ascending=[True, False])
interactions = interactions.drop_duplicates(subset=['user_id', 'item_id'])
interactions = interactions.drop('interaction', axis=1)

items = pd.read_csv('DataSet/item_profile.csv', sep='\t', header=0)
active_items = items[(items.active_during_test == 1)]
active_items_idx = active_items[['item_id', 'active_during_test']]
# Dictionary with only active items
active_items_to_recommend = {}
for item, state in active_items_idx.values:
    active_items_to_recommend[item] = state

print ("Create interact dictionary")
interact_dictionary = {}
for user, item, time in interactions.values:
    interact_dictionary.setdefault(user, {})[item] = time
for user in interact_dictionary:
    interact_dictionary[user] = OrderedDict(sorted(interact_dictionary[user].items(), key=lambda t: -t[1]))

print ("Create validation and training dictionary")
training_dictionary = {}
validation_dictionary = {}
i = 0
for user in interact_dictionary:
    count = 0
    print (i)
    i = i + 1
    validation_dictionary[user] = []
    training_dictionary[user] = []
    for item in interact_dictionary[user]:
        if count < 5:
            validation_dictionary[user].append(item)
        else:
            training_dictionary[user].append(item)
        count += 1
print validation_dictionary
print training_dictionary

print ("Writing result ")
out_file = open("TestDataSet/validationSet.csv", "w")
out_file.write('user_id,recommended_items\n')
for user in validation_dictionary:
    x = validation_dictionary[user]
    x = map(str, x)
    out_file.write(str(user) + ',' + ' '.join(x[:min(len(x), 5)]) + '\n')
out_file.close()

print ("Writing result ")
out_file = open("TestDataSet/trainingSet.csv", "w")
out_file.write('user_id\titem_id\tinteraction_type\n')
for user in training_dictionary:
    for item in training_dictionary[user]:
        out_file.write(str(user) + '\t' + str(item) + '\t' + str(1) + '\n')
out_file.close()