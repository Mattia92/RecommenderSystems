import graphlab
import pandas as pd
import graphlab.aggregate as agg

# pass in column names for each CSV and read them using pandas.
# Column names available in the readme file

#Reading users file:
users = pd.read_csv('DataSet/user_profile.csv', sep='\t', encoding='latin-1')

#Reading items file:
items = pd.read_csv('DataSet/item_profile.csv', sep='\t', encoding='latin-1', low_memory=False)

#Reading the target file:
filtered = graphlab.SFrame.read_csv('DataSet/target_users.csv')

#Reading the interactions file:
ratings_base = pd.read_csv('DataSet/interactions.csv', sep='\t')

#Since we be using GraphLab, lets convert these in SFrames
#We can use this data for training
ratings_base_SFrame = graphlab.SFrame(ratings_base)

#Create a recommender-friendly train-test split of the provided data set
train_data, test_data = graphlab.recommender.util.random_split_by_user(ratings_base_SFrame, max_num_users=1000,
                                                                       item_test_proportion=0.2)

##-----Popularity Recommender-----##
#######popularity_model = graphlab.popularity_recommender.create (train_data, user_id='user_id', item_id='item_id',
                                                           ######target='interaction_type')

###print popularity_model.evaluate_rmse(test_data, target='interaction_type')
########print("POPULARITY PREC RECALL")
##########print popularity_model.evaluate_precision_recall(test_data)


#Get recommendations for first 5 users and print them
#users = range(1,6) specifies user ID of first 5 users
#k=5 specifies top 5 recommendations to be given
############popularity_recomm = popularity_model.recommend(users=filtered, k=5)

##-----Item Similarity Recommender-----##
#######item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id',
                                                             ########target='interaction_type', similarity_type='pearson')
provina = pd.read_csv('DataSet/interactions.csv', sep='\t')
prova = graphlab.SFrame(provina)
prova.remove_column('interaction_type')
prova.remove_column('created_at')

item_sim_model = graphlab.item_similarity_recommender.create(train_data)
nn = item_sim_model.get_similar_items()

item_sim_model2 = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id',
                                                              target='interaction_type', nearest_items=nn)
item_sim_recomm2 = item_sim_model2.recommend(users=filtered, k=5)




###print item_sim_model.evaluate_rmse(test_data, target='interaction_type')
print("SIMILARITY PREC RECALL")
print item_sim_model2.evaluate_precision_recall(test_data)


#Make Recommendations:
##########item_sim_recomm = item_sim_model.recommend(users=filtered, k=5)

#######groupedResult = popularity_recomm \
   ####### .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    ########.sort('user_id')

# def split_string(x):
#     x = map(str, x)
#     return ' '.join(x)
#
# groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)
#
# groupedResult.export_csv('groupedResult.csv')


groupedResult = item_sim_recomm2 \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('groupedResult2.csv')