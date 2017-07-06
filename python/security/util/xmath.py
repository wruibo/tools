"""
    extend the math algorithms, including:
    1. normal interpolation algorithms
"""
import math


def avg(values):
    """
    compute average of sample values
    :param values: list, list of sample values
    :return: float, average of sample values
    """
    return sum(values) / len(values)


def var(values):
    """
    compute variance of sample values
    :param values: list, list of sample values
    :return: float, variance of sample values
    """
    # use average value of values as the expect value
    expect_value = avg(values)

    sum = 0.0
    for value in values:
        sum += (value-expect_value)**2

    return sum / (len(values)-1)


def stddev(values):
    '''
    compute standard deviation of sample values
    :param values: list, list of sample values
    :return: float, standard deviation of sample values
    '''
    return math.sqrt(var(values))


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
