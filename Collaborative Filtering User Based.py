import pickle as p
from collections import OrderedDict
user_prediction = p.load( open( "prediction.p", "rb" ) )

for user in user_prediction:
    print (user)
    user_prediction[user] = OrderedDict(sorted(user_prediction[user].items(), key=lambda t: t[1]))

print (user_prediction)
print (type(user_prediction))
#TODO: Retrieve first 5 predicion