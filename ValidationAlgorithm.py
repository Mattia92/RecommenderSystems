from __future__ import division

def apk(actual, predicted, k):
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
    k1 = min(min(k, len(predicted)), len(actual))
    # for i from 1 to 5(lenght of the predicted list if it is lass than 5)
    for i in range(1, k1):
        good_pred = 0 #numbers of correct predictions
        #for all the predictions to consider at point k find the number of good predictions
        for p in predicted[:i]:
            if p in actual:
                good_pred += 1
        prec = good_pred / i   #precision variable
        rec_old = rec_new      #recall at time k-1
        rec_new = good_pred / k1  #recall at time k
        sum += prec * (rec_new - rec_old)   #summarization

    print (sum)
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

# def MeanAveragePrecision(validation, result, at=5):
#     at = int(at)
#     average_precisions_sum = 0
#     count = 0
#     for user in validation:
#         count += 1
#         if not(result.has_key(user)):
#             continue
#         size = min(min(at, len(result[user])), len(validation[user]))
#         user_average_precision = 0
#         good_pred = 0
#         position = 1
#         for p in result[user][:size]:
#                 if p in validation[user]:
#                     good_pred += 1
#                     user_average_precision += good_pred / position
#                 position += 1
#             if (good_pred == 0):
#                 user_average_precision = 0
#             else:
#                 user_average_precision /= good_pred
#             average_precisions_sum += user_average_precision
#
#     map_at = average_precisions_sum / len(result)
#
#     return map_at


    #     node = entry[0]
    #     predictions = entry[1]
    #     correct = list(valid.get(node,dict()))
    #     total_correct = len(correct)
    #     if len(predictions) == 0 or total_correct == 0:
    #         average_precisions.append(0)
    #         continue
    #     running_correct_count = 0
    #     running_score = 0
    #     for i in range(min(len(predictions),at)):
    #         if predictions[i] in correct:
    #             correct.remove(predictions[i])
    #             running_correct_count += 1
    #             running_score += float(running_correct_count) / (i+1)
    #     average_precisions.append(running_score / min(total_correct, at))
    # return sum(average_precisions) / len(average_precisions)