from __future__ import print_function

import argparse
import time
import os

import numpy
import pandas
from scipy.sparse import coo_matrix
import annoy

from implicit import alternating_least_squares


def read_data(filename):
    """ Reads in the dataset, and returns a tuple of a pandas dataframe
    and a sparse matrix of item/user/interaction """
    # read in triples of user/item/interaction from the input dataset
    data = pandas.read_table(filename, usecols=[0, 1, 2], names=['user_id', 'item_id', 'interaction_type'])

    # map each artist and user to a unique numeric value
    data['user_id'] = data['user_id'].astype("category")
    data['item_id'] = data['item_id'].astype("category")

    # create a sparse matrix of all the users/plays
    interactions = coo_matrix((data['interaction_type'].astype(float),
                       (data['item_id'].cat.codes.copy(),
                        data['user_id'].cat.codes.copy())))

    return data, interactions


def bm25_weight(X, K1=100, B=0.8):
    """ Weighs each row of the sparse matrix of the data by BM25 weighting """
    # calculate idf per term (user)
    X = coo_matrix(X)
    N = X.shape[0]
    idf = numpy.log(float(N) / (1 + numpy.bincount(X.col)))

    # calculate length_norm per document (item)
    row_sums = numpy.ravel(X.sum(axis=1))
    average_length = row_sums.mean()
    length_norm = (1.0 - B) + B * row_sums / average_length

    # weight matrix rows by bm25
    X.data = X.data * (K1 + 1.0) / (K1 * length_norm[X.row] + X.data) * idf[X.col]
    return X


class TopRelated(object):
    def __init__(self, item_factors):
        # fully normalize item_factors, so can compare with only the dot product
        norms = numpy.linalg.norm(item_factors, axis=-1)
        self.factors = item_factors / norms[:, numpy.newaxis]

    def get_related(self, itemid, N=10):
        scores = self.factors.dot(self.factors[itemid])
        best = numpy.argpartition(scores, -N)[-N:]
        return sorted(zip(best, scores[best]), key=lambda x: -x[1])


class ApproximateTopRelated(object):
    def __init__(self, item_factors, treecount=20):
        index = annoy.AnnoyIndex(item_factors.shape[1], 'angular')
        for i, row in enumerate(item_factors):
            index.add_item(i, row)
        index.build(treecount)
        self.index = index

    def get_related(self, itemid, N=10):
        neighbours = self.index.get_nns_by_item(itemid, N)
        return sorted(((other, 1 - self.index.get_distance(itemid, other))
                      for other in neighbours), key=lambda x: -x[1])


def calculate_similar_items(input_filename, output_filename,
                              factors=50, regularization=0.01,
                              iterations=15,
                              exact=False, trees=20,
                              use_native=True,
                              dtype=numpy.float64):
    print ("Calculating similar items. This might take a while")
    print ("Reading data from ", input_filename)
    start = time.time()
    df, interactions = read_data(input_filename)
    print ("Read data file in ", time.time() - start)

    print ("Weighting matrix by bm25")
    weighted = bm25_weight(interactions)

    print ("Calculating factors")
    start = time.time()
    item_factors, user_factors = alternating_least_squares(weighted,
                                                             factors=factors,
                                                             regularization=regularization,
                                                             iterations=iterations,
                                                             use_native=use_native,
                                                             dtype=dtype)
    print ("Calculated factors in ", time.time() - start)

    # write out items by popularity
    print ("Calculating top items")
    # for each item_id count how many users have interact with it
    user_count = df.groupby('item_id').size()
    items = dict(enumerate(df['item_id'].cat.categories))
    # list dof items sorted by user_count
    to_generate = sorted(list(items), key=lambda x: -user_count[x])

    if exact:
        calc = TopRelated(item_factors)
    else:
        calc = ApproximateTopRelated(item_factors, trees)

    print("Writing top related to ", output_filename)
    with open(output_filename, "w") as o:
        for itemid in to_generate:
            item = items[itemid]
            for other, score in calc.get_related(itemid):
                o.write("%s\t%s\t%s\n" % (item, items[other], score))


def alternating_least_squares(Cui, factors, regularization=0.01,
                              iterations=15, use_native=True, num_threads=0,
                              dtype=numpy.float64):
    """ factorizes the matrix Cui using an implicit alternating least squares
    algorithm
    Args:
        Cui (csr_matrix): Confidence Matrix
        factors (int): Number of factors to extract
        regularization (double): Regularization parameter to use
        iterations (int): Number of alternating least squares iterations to run
        num_threads (int): Number of threads to run least squares iterations.
        0 means to use all CPU cores.
    Returns:
        tuple: A tuple of (row, col) factors
    """
    _check_open_blas()

    users, items = Cui.shape

    X = numpy.random.rand(users, factors).astype(dtype) * 0.01
    Y = numpy.random.rand(items, factors).astype(dtype) * 0.01

    Cui, Ciu = Cui.tocsr(), Cui.T.tocsr()

    #solver = _implicit.least_squares if use_native else least_squares
    solver = least_squares

    for iteration in range(iterations):
        s = time.time()
        solver(Cui, X, Y, regularization, num_threads)
        solver(Ciu, Y, X, regularization, num_threads)
        print ("Finished iteration " + str(iteration) + " in ", time.time() - s)

    return X, Y


def least_squares(Cui, X, Y, regularization, num_threads):
    """ For each user in Cui, calculate factors Xu for them
    using least squares on Y.
    Note: this is at least 10 times slower than the cython version included
    here.
    """
    users, factors = X.shape
    YtY = Y.T.dot(Y)

    for u in range(users):
        # accumulate YtCuY + regularization*I in A
        A = YtY + regularization * numpy.eye(factors)

        # accumulate YtCuPu in b
        b = numpy.zeros(factors)

        for i, confidence in nonzeros(Cui, u):
            factor = Y[i]
            A += (confidence - 1) * numpy.outer(factor, factor)
            b += confidence * factor

        # Xu = (YtCuY + regularization * I)^-1 (YtCuPu)
        X[u] = numpy.linalg.solve(A, b)


def nonzeros(m, row):
    """ returns the non zeroes of a row in csr_matrix """
    for index in range(m.indptr[row], m.indptr[row+1]):
        yield m.indices[index], m.data[index]


def _check_open_blas():
    """ checks to see if using OpenBlas. If so, warn if the number of threads isn't set to 1
    (causes perf issues) """
    if numpy.__config__.get_info('openblas_info') and os.environ.get('OPENBLAS_NUM_THREADS') != '1':
        print ("OpenBLAS detected. Its highly recommend to set the environment variable "
                 "'export OPENBLAS_NUM_THREADS=1' to disable its internal multithreading")


#-----MAIN-----#

calculate_similar_items('DataSet/interactionsClean.csv', 'DataSet/knn_sim_items.csv')