import pandas
it = pandas.read_csv('CF_Item_Based.csv')
us = pandas.read_csv('CF_User_Based.csv')
nullus = us.isnull().sum()
nullit = it.isnull().sum()

print ("UB:")
print (nullus)
print ("IB:")
print (nullit)