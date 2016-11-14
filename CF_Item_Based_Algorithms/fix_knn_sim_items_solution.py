import pandas as pd
import graphlab

# Reading the target file:
result = pd.read_csv('../Results/Result_NOT_Submit.csv', sep=',')
result_users = result.drop('recommended_items', 1)

# Reading the target file:
target_users = pd.read_table('../DataSet/target_usersClean.csv', usecols=[0], names=['user_id'])

addElements = pd.read_csv('../Results/submit_0_01072.csv', sep=',')

for index,row in result.iterrows():
    line = row[1]
    # Split the element of the string into a list
    line = line.split()
    if (len(line)<5):
        result = result.drop(index)
        result = result.append(addElements.loc[addElements['user_id'] == row[0]])

for index,row in addElements.iterrows():
    if not(row[0] in result['user_id'].values):
        result = result.append(row)
result = result.sort_values(by='user_id')

result = result.sort_values(by='user_id')
groupedResult = graphlab.SFrame(result)
groupedResult.export_csv('../Results/Fixed_Result.csv')