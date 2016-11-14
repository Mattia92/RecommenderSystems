# coding=utf-8
import pandas as pd
import graphlab.aggregate as agg

# Reading the target file:
target_users = pd.read_table('DataSet/target_usersClean.csv', usecols=[0], names=['user_id'])

# Reading items file:
items = pd.read_table('DataSet/item_profileClean.csv', usecols=[0, 12], names=['item_id', 'active'])
# Take only active items
items_active = items[items['active'] == 1]
#Reading interactions file to exclude
interactions_to_remove = pd.read_csv('DataSet/interactions.csv', sep='\t')
interactions_to_remove.drop(['interaction_type', 'created_at'], 1)
# Reading similar items file:
similaritems = pd.read_table('DataSet/knn_sim_items.csv', usecols=[0, 1, 2], names=['item_id', 'sim_item', 'score'])
# Consider only active items from the similar items file
similaritems = similaritems[similaritems['item_id'].isin(items_active['item_id'])]
# Consider only active similar items from the similar items file
similaritems = similaritems[similaritems['sim_item'].isin(items_active['item_id'])]
# Delete the item itself from its similar items
#----Non so se questa cosa è giusta perchè forse per ogni item_id cancella tutti i sim_item, non solo il suo
similaritems = similaritems[similaritems['item_id'] != similaritems['sim_item']]

# Reading interactions file:
interactions = pd.read_table('DataSet/interactionsClean.csv', usecols=[0, 1], names=['user_id', 'item_id'])
interactions_sorted_by_users = interactions.sort_values(by='user_id')
interactions_sorted_by_target_users = interactions_sorted_by_users[interactions_sorted_by_users['user_id'].
                                                                    isin(target_users['user_id'])]

# d = pd.DataFrame(columns=['user_id', 'item_id', 'score'])
#
# for index, row in interactions_sorted_by_target_users.iterrows():
#     for index, s in similaritems.iterrows():
#         if s['item_id'] == row['item_id']:
#             d.append([row['user_id'], s['sim_item'], s['score']])
#
# d.sort(['user_id', 'score'], ascending=[True, False])
#
# d.to_csv(path_or_buf = 'users_sim_items.csv', sep = '\t', index=False)

# Reading the new csv file created
df = pd.read_csv('users_sim_items.csv', sep='\t')
# Dropping the score column
df.drop('score', 1)

#Dropping the items tih wich the user has interacted
for x in df.iterrows():
    if interactions_to_remove.isin(x):
        df.drop(x)

us = None
# Selecting only the first five items to reccomend dropping the others
for y in df.iterrows():
    if us == None or not y['user_id'] == us:
        count = 0
        us = y['user_id']
    elif y['user_id'] == us and count < 5:
        count = count + 1
    elif y['user_id'] == us and count >= 5:
        df.drop(y)

#Grouping the recommended items, hoping this is the correct operation :D
df.groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')})

# TODO:
# Per ogni user in interactions_sorted_by_target_users prendere l'item con cui interagisce e andare
# a prendere i suoi similar items in similaritems con punteggio
# Raggruppare gli user e nella lista di similar item fare un ordinamento secondo il punteggio
# Prendere i top 5 similar items
# Scrivere il file csv finale
# PREGARE CHE TUTTO FUNZIONI E VENGA FUORI UN PUNTEGGIO DECENTE!!!!
