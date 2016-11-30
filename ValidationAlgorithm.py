import numpy as np

def apk(actual, predicted, k, num_users_interactions):
    """
    Computes the average precision at k.
    This function computes the average precision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    #if len(predicted)>k:
    #    predicted = predicted[:k]

    #inizialize all the variables needed
    sum = 0
    prec = 0.0
    rec_old = 0.0
    rec_new = 0.0
    # for i from 1 to 5(lenght of the predicted list if it is lass than 5)
    for i in range(1,min(k, len(predicted))):
        good_pred = 0 #numbers of correct predictions
        #for all the predictions to consider at point k find the number of good predictions
        for p in predicted[:i]:
            if p in actual:
                good_pred += 1
        prec = good_pred / k   #precision variable
        rec_old = rec_new      #recall at time k-1
        rec_new = good_pred / num_users_interactions  #recall at time k
        sum += prec * (rec_new - rec_old)   #summarization
        print rec_new

    return sum

    # score = 0.0
    # num_hits = 0.0
    #
    # for i,p in enumerate(predicted):
    #     if p in actual and p not in predicted[:i]:
    #         num_hits += 1.0
    #         score += num_hits / (i+1.0)
    #
    # if not actual:
    #     return 0.0
    #
    # return score / min(len(actual), k)

def mapk(actual, predicted, k=5):
    """
    Computes the mean average precision at k.
    This function computes the mean average precision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


def MeanAveragePrecision(valid_filename, attempt_filename, at=10):
    at = int(at)
    valid = dict()
    for line in csv.DictReader(open(valid_filename,'r')):
        valid.setdefault(line['source_node'],set()).update(line['destination_nodes'].split(" "))
    attempt = list()
    for line in csv.DictReader(open(attempt_filename,'r')):
        attempt.append([line['source_node'], line['destination_nodes'].split(" ")])
    average_precisions = list()
    for entry in attempt:
        node = entry[0]
        predictions = entry[1]
        correct = list(valid.get(node,dict()))
        total_correct = len(correct)
        if len(predictions) == 0 or total_correct == 0:
            average_precisions.append(0)
            continue
        running_correct_count = 0
        running_score = 0
        for i in range(min(len(predictions),at)):
            if predictions[i] in correct:
                correct.remove(predictions[i])
                running_correct_count += 1
                running_score += float(running_correct_count) / (i+1)
        average_precisions.append(running_score / min(total_correct, at))
    return sum(average_precisions) / len(average_precisions)