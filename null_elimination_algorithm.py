import graphlab
import pandas as pd
import numpy
import math

def convert(x):
    try:
        return x.astype(int)
    except:
        return x

users = pd.read_csv('DataSet/user_profile.csv', sep='\t')
items = pd.read_csv('DataSet/item_profile.csv', sep='\t')

for column in users:

    c = users[column]
    count = 0
    sum = 0

    if c.dtype == numpy.int64 or c.dtype == numpy.float64:
        for x in c.iteritems():
            if not math.isnan(x[1]):
                sum = sum + x[1]
                count = count +1
        r = int(sum/count)
        for x in c.iteritems():
            if math.isnan(x[1]):
                users.set_value(x[0], column, r)

for column in items:

    i = items[column]
    count = 0
    sum = 0

    if i.dtype == numpy.int64:
        for x in i.iteritems():
            if not math.isnan(x[1]):
                sum = sum + x[1]
                count = count +1

        r = int(sum/count)

        for x in i.iteritems():
            if math.isnan(x[1]):
                items.set_value(x[0], column, r)

    if i.dtype == numpy.float64:
        for x in i.iteritems():
            if not math.isnan(x[1]):
                sum = sum + x[1]
                count = count +1

        r = sum/count
        round(r , ndigits=1)

        for x in i.iteritems():
            if math.isnan(x[1]):
                items.set_value(x[0], column, r)

users.apply(convert).to_csv(path_or_buf = 'user_profile_no_null.csv', sep = '\t')

items.to_csv(path_or_buf = 'item_profile_no_null.csv', sep = '\t')