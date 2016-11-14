import pandas as pd
import string

# Reading the target file:
result = pd.read_csv('../Results/Result_NOT_Submit.csv', sep=',')
result_users = result.drop('recommended_items', 1)

# Reading the target file:
target_users = pd.read_table('../DataSet/target_usersClean.csv', usecols=[0], names=['user_id'])

addElements = pd.read_csv('../Results/submit_0_01072.csv', sep=',')
print result

for index,row in addElements.iterrows():
    if not(row[0] in result['user_id']):
        result = result.append(row)
result = result.sort_values(by='user_id')
print result
    #line = result.get_value(idx, 'user_id')

# line = result.get_value(1, 'recommended_items')
# print(line)
# # Split the element of the string into a list
# line = line.split()
# print (len(line))
