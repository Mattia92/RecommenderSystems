# coding=utf-8
import pandas as pd
import graphlab
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

result = pd.merge(left=interactions_sorted_by_target_users, right=similaritems, on='item_id')
result = result.drop('item_id', 1)
result = result.sort(['user_id', 'score'], ascending=[True, False])
result = result.drop_duplicates()
result = result.drop('score', 1)

print (result.shape)

us = None
i = 1
# Selecting only the first five items to recommend dropping the others
for index,y in result.iterrows():
    print ("Iteration: " + str(i))
    i = i + 1
    if us == None or not y[0] == us:
        count = 0
        us = y[0]
    elif y[0] == us and count < 4:
        count = count + 1
    elif y[0] == us and count >= 4:
        result = result.drop(index)

recomm = graphlab.SFrame(result)
groupedResult = recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('sim_item')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('./Results/Result_NOT_Submit.csv')