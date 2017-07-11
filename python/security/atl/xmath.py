"""
    extend the math algorithms, including:
    1. normal interpolation algorithms
"""
import math


def avg(a=[]):
    """
    compute average of sample values
    :param values: list, list of sample values
    :return: float, average of sample values
    """
    if len(a) == 0:
        return

    return float(sum(a)) / len(a)


def var(a=[]):
    """
    compute variance of sample values
    :param values: list, list of sample values
    :return: float, variance of sample values
    """
    if len(a) == 0:
        return

    # use average value of values as the expect value
    expect_value = avg(a)

    sum = 0.0
    for value in a:
        sum += (value-expect_value)**2

    return sum / (len(a)-1)


def stddev(a=[]):
    '''
    compute standard deviation of sample values
    :param values: list, list of sample values
    :return: float, standard deviation of sample values
    '''
    if len(a) == 0:
        return

    return math.sqrt(var(a))


def cov(a1, a2):
    """
    compute the covariance of sample a1 and a2
    :param a1: list, list of input data values
    :param a2: list, list of input data values
    :return: float, covariance of sample a1 and a2
    """
    if len(a1) != len(a2):
        return None

    expect_value1 = avg(a1)
    expect_value2 = avg(a1)

    sum = 0.0
    idx = num = len(a1)
    while idx > 0:
        idx -= 1
        sum += (a1[idx]-expect_value1)*(a1[idx]-expect_value2)

    return sum / (num-1)


def cor(a1, a2):
    """
     compute the correlation of sample a1 and a2, using pearson correlation algorithm
     :param a1: list, list of input data values
     :param a2: list, list of input data values
     :return:
    """
    if len(a1) != len(a2):
     return None

    # compute covariance of a1 and a2
    cov12 = cov(a1, a2)

    # compute the standard deviation of a1, a2
    stddev1 = stddev(a1)
    stddev2 = stddev(a2)

    return cov12/(stddev1*stddev2)


def rotate(m=[[]]):
    """
        rotate matrix with its ranks, rows to columns and columns to rows, example:
    before transform, there are N column list like:

         column1 column2 ... columnN
           v11    v21          vN1
           v12    v22          vN2
            .      .            .
            .      .            .
            .      .            .
           v1M     v2M          VNM

    after transform, the result is:

      row1 v11    v21          vN1
      row2 v12    v22          vN2
            .      .            .
            .      .            .
            .      .            .
      rowM v1M     v2M          VNM
    :param m: matrix
    :return: rotated matrix
    """

    rotated_matrix = []

    for i in range(0, len(m[0])):
        values = []
        for j in range(0, len(m)):
            values.append(m[j][i])
        rotated_matrix.append(values)

    return rotated_matrix
