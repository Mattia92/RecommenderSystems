import graphlab
import pandas as pd
import graphlab.aggregate as agg

# pass in column names for each CSV and read them using pandas.
# Column names available in the readme file

#Reading users file:
users = pd.read_csv('DataSet/user_profile.csv', sep='\t', encoding='latin-1')

#Reading items file:
items = pd.read_csv('DataSet/item_profile.csv', sep='\t', encoding='latin-1', low_memory=False)

#Reading the interactions file:
ratings_base = pd.read_csv('DataSet/interactions.csv', sep='\t')

filtered = graphlab.SFrame.read_csv('DataSet/target_users.csv')

#Since we be using GraphLab, lets convert these in SFrames
#We can use this data for training

train_data = graphlab.SFrame(ratings_base)

popularity_model = graphlab.popularity_recommender.create (train_data, user_id='user_id', item_id='item_id', target='interaction_type')
#Get recommendations for first 5 users and print them
#users = range(1,6) specifies user ID of first 5 users
#k=5 specifies top 5 recommendations to be given
popularity_recomm = popularity_model.recommend(users=filtered, k=5)

#Train Model
item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id',
                                                             target='interaction_type', similarity_type='pearson')
#item_sim_model_figo = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id',
                                                             #target='interaction_type', user_data=users, item_data=items,
                                                             #similarity_type='pearson')
print item_sim_model.evaluate_rmse()


#Make Recommendations:
item_sim_recomm = item_sim_model.recommend(users=filtered, k=5)

groupedResult = popularity_recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('groupedResult.csv')



groupedResult = item_sim_recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('groupedResult2.csv')