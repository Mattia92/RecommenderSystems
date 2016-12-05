import pandas as pd
import math
import numpy
import CBAlgorithms

CB_UU_similarity_shrink = 10

target_users = pd.read_csv('DataSet/target_users.csv')
for i, row in target_users.iterrows():
    if row['user_id'] == 2613732:
        print "ciao"
print 2613732 in target_users['user_id']

user_cols = ['user', 'job', 'career', 'discipline', 'industry', 'country', 'region', 'experience', 'exp_years', 'exp_years_current',
                   'edu_deg', 'edu_fiel']
user_profile = pd.read_csv('DataSet/user_profile.csv', sep='\t',names=user_cols, header=0)

# Create the dictionary needed to compute the similarity between users
# It is the User content matric build with dictionaries
# Dictionary is a list of elements, each element is defined as following
# dict {user -> (list of {attribute -> 1})}
users_attributes = {}
#for each row of the user_profile csv
for i, row in user_profile.iterrows():
    #initialize the dictionary of the user
    users_attributes[row['user']] = {}
    #for each attribute of the user
    for att in user_cols:
        if not(att == 'user'):
             #if the attribute is jobroles then split the string obtaining the various jobs and insert them in the dictionary
             #if the value of the field jobroles is 0 insert nothing
             if (att == 'job'):
                 if not(row[att] == '0'):
                    jobs = str(row[att]).split(",")
                    for j in jobs:
                        users_attributes[row['user']][att + '_' + str(j)] = 1
             # if the attribute is edu_fieldofstudies then split the string obtaining the various fields and insert them in
             # the dictionary
             elif(att == 'edu_fiel'):
                 if type(row[att]) == str:
                     fields = str(row[att]).split(",")
                     for f in fields:
                         users_attributes[row['user']][att + '_' + str(f)] = 1
             # if the attribute is country dont't consider float values
             elif(att == 'country'):
                 if type(row[att]) == str:
                     users_attributes[row['user']][att + '_' + str(row[att])] = 1
             #if the column type is int or float discard Null values
             elif(user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                 if not(math.isnan(row[att])):
                     users_attributes[row['user']][att + '_' + str(row[att])] = 1
             else:
                 users_attributes[row['user']][att + '_' + str(row[att])] = 1

# Create the dictionary containing for each attribute the list of users which have it
# Dictionary is a list of elements, each element is defined as following
# dict {attribute -> (list of {user -> 1})}
attributes_users = {}
#for each row of the user_profile csv
for i, row in user_profile.iterrows():
    #for each attribute of the user
    for att in user_cols:
        if not(att == 'user'):
             #if the attribute is jobroles then split the string obtaining the various jobs and insert them in the dictionary
             #if the value of the field jobroles is 0 insert nothing
             if (att == 'job'):
                 if not(row[att] == '0'):
                    jobs = str(row[att]).split(",")
                    for j in jobs:
                        # if the dictionary is not already inizialized do it
                        if not attributes_users.has_key(att + '_' + str(j)):
                            attributes_users[att + '_' + str(j)] = {}
                        attributes_users[att + '_' + str(j)][row['user']] = 1
             # if the attribute is edu_fieldofstudies then split the string obtaining the various fields and insert them in
             # the dictionary
             elif(att == 'edu_fiel'):
                 if type(row[att]) == str:
                     fields = str(row[att]).split(",")
                     for f in fields:
                         if not attributes_users.has_key(att + '_' + str(f)):
                             attributes_users[att + '_' + str(f)] = {}
                         attributes_users[att + '_' + str(f)][row['user']] = 1
             # if the attribute is country dont't consider float values
             elif(att == 'country'):
                 if type(row[att]) == str:
                     if not attributes_users.has_key(att + '_' + str(row[att])):
                         attributes_users[att + '_' + str(row[att])] = {}
                     attributes_users[att + '_' + str(row[att])][row['user']] = 1
             #if the column type is int or float discard Null values
             elif(user_profile[att].dtype == numpy.int64 or user_profile[att].dtype == numpy.float64):
                 if not(math.isnan(row[att])):
                     if not attributes_users.has_key(att + '_' + str(row[att])):
                         attributes_users[att + '_' + str(row[att])] = {}
                     attributes_users[att + '_' + str(row[att])][row['user']] = 1
             else:
                 if not attributes_users.has_key(att + '_' + str(row[att])):
                     attributes_users[att + '_' + str(row[att])] = {}
                 attributes_users[att + '_' + str(row[att])][row['user']] = 1

CB_user_user_similarity_dictionary = CBAlgorithms.CBUserUserSimilarity(target_users, users_attributes, attributes_users, CB_UU_similarity_shrink)

