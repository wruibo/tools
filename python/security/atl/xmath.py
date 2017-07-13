"""
    extend the math algorithms, including:
    1. normal interpolation algorithms
"""
import math


def avg(arr):
    """
        compute average of array values
    :param values: list, list of array values
    :return: float, average of array values
    """
    if len(arr) == 0:
        raise "empty input array has no average value."

    return float(sum(arr)) / len(arr)


def var(a=[]):
    """
        compute variance of array values
    :param values: list, list of array values
    :return: float, variance of array values
    """
    if len(a) == 0:
        raise "empty input array has no variance value."

    # use average value of values as the expect value
    expect_value = avg(a)

    sum = 0.0
    for value in a:
        sum += (value-expect_value)**2

    return sum / (len(a)-1)


def stddev(a=[]):
    '''
        compute standard deviation of array values
    :param values: list, list of array values
    :return: float, standard deviation of array values
    '''
    if len(a) == 0:
        raise "empty input array has no standard deviation value."

    return math.sqrt(var(a))


def cov(a1, a2):
    """
        compute the covariance of array a1 and a2
    :param a1: list, list of input data values
    :param a2: list, list of input data values
    :return: float, covariance of array a1 and a2
    """
    if len(a1) != len(a2):
        raise "covariance needs 2 length equal arrays, input array is %d and %d." % (len(a1), len(a2))

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
        compute the correlation of array a1 and a2, using pearson correlation algorithm
     :param a1: list, list of input data values
     :param a2: list, list of input data values
     :return:
    """
    if len(a1) != len(a2):
        raise "correlation needs 2 length equal arrays, input array is %d and %d." % (len(a1), len(a2))

    # compute covariance of a1 and a2
    cov12 = cov(a1, a2)

    # compute the standard deviation of a1, a2
    stddev1 = stddev(a1)
    stddev2 = stddev(a2)

    return cov12/(stddev1*stddev2)

def multi(a):
    """
        multiple for
    :param a:
    :return:
    """
    pass