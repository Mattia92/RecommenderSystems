import graphlab
import pandas as pd
import graphlab.aggregate as agg

# pass in column names for each CSV and read them using pandas.
# Column names available in the readme file

#Reading users file:
users = pd.read_csv('DataSet/user_profile.csv', sep='\t', encoding='latin-1')


#Reading items file:
items = pd.read_csv('DataSet/item_profile.csv', sep='\t', encoding='latin-1', low_memory=False)


item = graphlab.SFrame.read_csv('DataSet/item_profile.csv', sep='\t',)
itemfiltered = item.filter_by(0, 'active_during_test', exclude=True)

itemfilt = itemfiltered.remove_columns(['title', 'career_level', 'discipline_id', 'industry_id', 'country', 'region',
                                        'latitude', 'longitude', 'employment', 'tags', 'created_at', 'active_during_test'])

#Reading the target file:
filtered = graphlab.SFrame.read_csv('DataSet/target_users.csv')

#Reading the interactions file:
ratings_base = pd.read_csv('DataSet/interactions.csv', sep='\t')

#Reading the interactions file for the recommendation to remove
interactionsToRemove = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')
interactionsToRemove.remove_columns(['interaction_type', 'created_at'])

#Since we be using GraphLab, lets convert these in SFrames
#We can use this data for training
ratings_base_SFrame = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')

item_sim_model = graphlab.item_similarity_recommender.create(ratings_base_SFrame, item_id='item_id', user_id='user_id')
recomm = item_sim_model.recommend(users=filtered, items=itemfilt, k=5, exclude=interactionsToRemove, random_seed=911)

# m1 = graphlab.ranking_factorization_recommender.create(train_data, target='interaction_type')
# recomm = m1.recommend(users=filtered, k=5)
# print("SIMILARITY 1 PREC RECALL")
# print m1.evaluate_precision_recall(test_data)

#m3 = graphlab.ranking_factorization_recommender.create(ratings_base_SFrame, target='interaction_type',
                                                       #ranking_regularization = 0.1, unobserved_rating_value = 1)
#m3 = graphlab.ranking_factorization_recommender.create(ratings_base_SFrame, target='rating', solver = 'ials')

#recomm = m3.recommend(users=filtered, k=5)

# nn1 = item_sim_model.get_similar_items()
# nn2 = item_sim_model.get_similar_items()
#
# item_sim_model_final1 = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='item_id',
#                                                               target='interaction_type', nearest_items=nn1)
# item_sim_model_final2 = graphlab.item_similarity_recommender.create(ratings_base_SFrame, user_id='user_id', item_id='item_id',
#                                                               target='interaction_type', nearest_items=nn2)
# item_sim_recomm1 = item_sim_model_final1.recommend(users=filtered, k=5)
# item_sim_recomm2 = item_sim_model_final2.recommend(users=filtered, k=5)


###print item_sim_model.evaluate_rmse(test_data, target='interaction_type')
# print("SIMILARITY 1 PREC RECALL")
# print item_sim_model_final1.evaluate_precision_recall(test_data)
#
# print("SIMILARITY 2 PREC RECALL")
# print item_sim_model_final2.evaluate_precision_recall(test_data)

groupedResult = recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('ItemSimTwoFilter.csv')

