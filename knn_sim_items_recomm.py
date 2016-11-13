from __future__ import print_function
import pandas as pd

#Reading the target file:
target_users = pd.read_table('DataSet/target_usersClean.csv', usecols=[0], names=['user_id'])

#Reading items file:
items = pd.read_table('DataSet/item_profileClean.csv', usecols=[0, 12], names=['item_id', 'active'])
items_active = items[items['active'] == 1]

#Reading interactions file:
interactions = pd.read_table('DataSet/interactionsClean.csv', usecols=[0, 1], names=['user_id', 'item_id'])
interactions_sorted_by_users = interactions.sort_values(by='user_id')

#TODO:
#per ogni user in target_users si devono prendere gli items da interactions_sorted_by_users
#per ogni item si devono recuperare gli items simili e il punteggio dal file knn_sim_items.csv
#ricordarsi di eliminare l'item stesso dalla lista di items simili (il ptimo che ha sempre il punteggio maggiore)
#ordinare la lista in base al punteggio
#per ogni user prendere i 5 items con punteggio più alto
#scrivere il file csv finale