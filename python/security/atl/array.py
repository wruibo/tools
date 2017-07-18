"""
    array process methods, array like:
        [v1, v2, ..., vn]
    is an length with n elements array
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


def var(arr):
    """
        compute variance of array values
    :param values: list, list of array values
    :return: float, variance of array values
    """
    if len(arr) == 0:
        raise "empty input array has no variance value."

    # use average value of values as the expect value
    expect_value = avg(arr)

    sum = 0.0
    for value in arr:
        sum += (value-expect_value)**2

    return sum / (len(arr)-1)


def stddev(arr):
    '''
        compute standard deviation of array values
    :param values: list, list of array values
    :return: float, standard deviation of array values
    '''
    if len(arr) == 0:
        raise "empty input array has no standard deviation value."

    return math.sqrt(var(arr))


def cov(arr1, arr2):
    """
        compute the covariance of array arr1 and arr2
    :param arr1: list, list of input data values
    :param arr2: list, list of input data values
    :return: float, covariance of array arr1 and arr2
    """
    if len(arr1) != len(arr2):
        raise "covariance needs 2 length equal arrays, input array is %d and %d." % (len(arr1), len(arr2))

    expect_value1 = avg(arr1)
    expect_value2 = avg(arr1)

    sum = 0.0
    idx = num = len(arr1)
    while idx > 0:
        idx -= 1
        sum += (arr1[idx]-expect_value1)*(arr1[idx]-expect_value2)

    return sum / (num-1)


def cor(arr1, arr2):
    """
        compute the correlation of array arr1 and arr2, using pearson correlation algorithm
     :param arr1: list, list of input data values
     :param arr2: list, list of input data values
     :return:
    """
    if len(arr1) != len(arr2):
        raise "correlation needs 2 length equal arrays, input array is %d and %d." % (len(arr1), len(arr2))

    # compute covariance of arr1 and arr2
    cov12 = cov(arr1, arr2)

    # compute the standard deviation of arr1, arr2
    stddev1 = stddev(arr1)
    stddev2 = stddev(arr2)

    return cov12/(stddev1*stddev2)


def sub(arr, withval):
    """
        sub array data with specified value or another aray
    :param arr: list, which will subtract @withval
    :param withval: list or value, which will be subtract with
    :return: array
    """
    result = []

    if isinstance(withval, list) or isinstance(withval, tuple):
        if len(withval) != len(arr):
            raise "array subtract array need the same length."

        for i in range(0, len(arr)):
            result.append(arr[i] - withval[i])
    else:
        for i in range(0, len(arr)):
            result.append(arr[i] - withval)

    return result


def multi(arr, withval=None):
    """
        multiple data in array with other values
    :param arr: array
    :param withval: array, object or None
    :return: multiple result
    """
    if withval is None: # multiple each data in array
        result = None
        for elmt in arr:
            if result is None:
                result = elmt
            else:
                result *= elmt
        return result
    else: #multiple array data with other values
        result = []

        if isinstance(withval, list) or isinstance(withval, tuple):
            if len(withval) != len(arr):
                raise "array multiple array need the same length."
            for i in range(0, len(arr)):
                result.append(arr[i]*withval[i])
        else:
            for elmt in arr:
                result.append(elmt*withval)

        return result
