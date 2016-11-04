import CollaborativeFilteringPackage as cfp
import pandas as pd

users = pd.read_csv('DataSet/user_profile.csv', sep='\t', encoding='latin-1')

prefs = cfp.loadDataset()

print prefs['285']

for person in open("DataSet/target_usersClean.csv"):
    print (person)
    person.rstrip()
    #res = cfp.getRecommendations(prefs, person, similarity='sim_distance')
    res = cfp.topMatches(prefs, person, n=5)

print (res)


# for person1 in filtered:
#     p1_id = person1.get('user_id')
#     for person2 in users:
#         p2_id = person2.get('user_id')
#         if p2_id != p1_id:
