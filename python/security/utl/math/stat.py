"""
    math of statistic
"""
import math


def avg(seq):
    """
        compute average of array values
    :param seq: list, list of array values
    :return: float, average of array values
    """
    return float(sum(seq)) / len(seq)


def mean(seq):
    """
        compute mean value of random sequence
    :param seq: array, random sequence values
    :return: float, mean value
    """
    return avg(seq)


def var(seq, sample=True):
    """
        compute variance of array values
    :param seq: list, list of array values
    :return: float, variance of array values
    """
    # use average value of values as the expect value
    expect_value = avg(seq)

    sum, num = 0.0, len(seq)
    for value in seq:
        sum += (value-expect_value)**2

    return sum / (num-1) if sample else sum / num


def stddev(seq, sample=True):
    '''
        compute standard deviation of array values
    :param seq: list, list of array values
    :return: float, standard deviation of array values
    '''
    return math.sqrt(var(seq, sample))


def cov(seq1, seq2, sample=True):
    """
        compute the covariance of array a1 and a2
    :param seq1: list, list of input data values
    :param seq2: list, list of input data values
    :return: float, covariance of array a1 and a2
    """
    if len(seq1) != len(seq2):
        raise ValueError("covariance needs 2 length equal arrays, input array is %d and %d." % (len(seq1), len(seq2)))

    expect_value1 = avg(seq1)
    expect_value2 = avg(seq1)

    sum = 0.0
    idx = num = len(seq1)
    while idx > 0:
        idx -= 1
        sum += (seq1[idx]-expect_value1)*(seq2[idx]-expect_value2)

    return sum / (num-1) if sample else sum / num


def cor(seq1, seq2, sample=True):
    """
        compute the correlation of array a1 and a2, using pearson correlation algorithm
     :param seq1: list, list of input data values
     :param seq2: list, list of input data values
     :return:
    """
    if len(seq1) != len(seq2):
        raise ValueError("correlation needs 2 length equal arrays, input array is %d and %d." % (len(seq1), len(seq2)))

    # compute covariance of a1 and a2
    cov12 = cov(seq1, seq2, sample)

    # compute the standard deviation of a1, a2
    stddev1 = stddev(seq1, sample)
    stddev2 = stddev(seq2, sample)

    return cov12/(stddev1*stddev2)
