# coding=utf-8
from __future__ import print_function
import pandas as pd

# Reading the target file:
target_users = pd.read_table('DataSet/target_usersClean.csv', usecols=[0], names=['user_id'])

# Reading items file:
items = pd.read_table('DataSet/item_profileClean.csv', usecols=[0, 12], names=['item_id', 'active'])
# Take only active items
items_active = items[items['active'] == 1]

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

# TODO:
# Per ogni user in interactions_sorted_by_target_users prendere l'item con cui interagisce e andare
# a prendere i suoi similar items in similaritems con punteggio
# Raggruppare gli user e nella lista di similar item fare un ordinamento secondo il punteggio
# Prendere i top 5 similar items
# Scrivere il file csv finale
# PREGARE CHE TUTTO FUNZIONI E VENGA FUORI UN PUNTEGGIO DECENTE!!!!
