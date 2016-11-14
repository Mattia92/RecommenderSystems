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
similaritems = similaritems[similaritems['item_id'] != similaritems['sim_item']]

# Reading interactions file:
interactions = pd.read_table('DataSet/interactionsClean.csv', usecols=[0, 1], names=['user_id', 'item_id'])
interactions_sorted_by_users = interactions.sort_values(by='user_id')

# TODO:
# per ogni user in target_users si devono prendere gli items da interactions_sorted_by_users
# ordinare la lista in base al punteggio
# per ogni user prendere i 5 items con punteggio più alto
# scrivere il file csv finale
