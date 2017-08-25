"""
    extend the math algorithms, including:
    1. normal interpolation algorithms
"""
import math


def avg(arr):
    """
        compute average of array values
    :param arr: list, list of array values
    :return: float, average of array values
    """
    return float(sum(arr)) / len(arr)


def var(arr, sample=True):
    """
        compute variance of array values
    :param arr: list, list of array values
    :return: float, variance of array values
    """
    # use average value of values as the expect value
    expect_value = avg(arr)

    sum, num = 0.0, len(arr)
    for value in arr:
        sum += (value-expect_value)**2

    return sum / (num-1) if sample else sum / num


def stddev(arr, sample=True):
    '''
        compute standard deviation of array values
    :param arr: list, list of array values
    :return: float, standard deviation of array values
    '''
    return math.sqrt(var(arr, sample))


def cov(arr1, arr2, sample=True):
    """
        compute the covariance of array a1 and a2
    :param arr1: list, list of input data values
    :param arr2: list, list of input data values
    :return: float, covariance of array a1 and a2
    """
    if len(arr1) != len(arr2):
        raise Exception("covariance needs 2 length equal arrays, input array is %d and %d." % (len(arr1), len(arr2)))

    expect_value1 = avg(arr1)
    expect_value2 = avg(arr1)

    sum = 0.0
    idx = num = len(arr1)
    while idx > 0:
        idx -= 1
        sum += (arr1[idx]-expect_value1)*(arr2[idx]-expect_value2)

    return sum / (num-1) if sample else sum / num


def cor(arr1, arr2, sample=True):
    """
        compute the correlation of array a1 and a2, using pearson correlation algorithm
     :param arr1: list, list of input data values
     :param arr2: list, list of input data values
     :return:
    """
    if len(arr1) != len(arr2):
        raise ("correlation needs 2 length equal arrays, input array is %d and %d." % (len(arr1), len(arr2)))

    # compute covariance of a1 and a2
    cov12 = cov(arr1, arr2, sample)

    # compute the standard deviation of a1, a2
    stddev1 = stddev(arr1, sample)
    stddev2 = stddev(arr2, sample)

    return cov12/(stddev1*stddev2)


def add(arr, withval):
    """
        add array data with specified value or another array
    :param arr: list, which will subtract @withval
    :param withval: list or value, which will be subtract with
    :return: array
    """

    result = []

    if isinstance(withval, list) or isinstance(withval, tuple):
        if len(withval) != len(arr):
            raise Exception("array add array need the same length.")
        for i in range(0, len(arr)):
            result.append(arr[i] + withval[i])
    else:
        for i in range(0, len(arr)):
            result.append(arr[i] + withval)

    return result


def sub(arr, withval):
    """
        sub array data with specified value or another array
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


def multi(arr, withval):
    """
        multiple data in array with other values
    :param arr: array
    :param withval: array, object or None
    :return: multiple result
    """
    result = []

    if isinstance(withval, list) or isinstance(withval, tuple):
        if len(withval) != len(arr):
            raise "array multiple array need the same length."
        for i in range(0, len(arr)):
            result.append(arr[i]*withval[i])
    else:
        if isinstance(arr, list) or isinstance(arr, tuple):
            for elmt in arr:
                result.append(elmt*withval)
        else:
            result = arr*withval

    return result


def divide(arr, withval):
    """
        divide data in array with other values
    :param arr: array
    :param withval: array, object or None
    :return: multiple result
    """
   #divide array data with other values
    result = []

    if isinstance(withval, list) or isinstance(withval, tuple):
        if len(withval) != len(arr):
            raise "array divide array need the same length."
        for i in range(0, len(arr)):
            result.append(arr[i]/withval[i])
    else:
        for elmt in arr:
            result.append(elmt/withval)

    return result


def sum(arr):
    """
        compute sum of data in array
    :param arr: array
    :return: product result
    """
    result = None
    for elmt in arr:
        if result is None:
            result = elmt
        else:
            result += elmt
    return result


def product(arr):
    """
        compute product of data in array
    :param arr: array
    :return: product result
    """
    result = None
    for elmt in arr:
        if result is None:
            result = elmt
        else:
            result *= elmt
    return result


def combine(arr, num):
    """
        generate the combination of input array with specified combination number
    :param arr: list, set for combination
    :param num: int, combine number want from array
    :return: list, combination results
    """
    # recurse terminate condition
    if num < 1:
        raise "combine number for array can not be less than 1"

    if len(arr)==num:
        return [arr]

    if num==1:
        return [[item] for item in arr]

    # combine results
    results = []

    for i in range(0, len(arr)):
        # arr except item i
        itemi = arr[i]
        leftarr = arr[i+1:len(arr)]

        # choose current item for combination
        leftcombs = combine(leftarr, num-1)
        for leftcomb in leftcombs:
            comb = [itemi] + leftcomb
            results.append(comb)

    return results


def permute(arr, num):
    """
        generate the permutation of input array with specified permutation number
    :param arr: list, set for permutation
    :param num: int, permute number want from array
    :return: list, permutation results
    """
    # recurse terminate condition
    if num < 1:
        raise "permute number for array can not be less than 1"

    if num==1:
        return [[item] for item in arr]

    # combine results
    results = []

    for i in range(0, len(arr)):
        # arr except item i
        itemi = arr[i]
        leftarr = arr[0:i] + arr[i+1:len(arr)]

        # choose current item for permutation
        leftcombs = permute(leftarr, num-1)
        for leftcomb in leftcombs:
            results.append([itemi] + leftcomb)

    return results


def combines(*arrs):
    """
        equal probability combine items for input arrays, the input array must be same dimension, e.g.:
    input:
        [x1, x2, x3, x4], [y1, y2, y3, y4]
    output
        [
            [ [x1, y1], [x1, y2], [x1, y3], [x1, y4] ]
            [ [x2, y1], [x2, y2], [x2, y3], [x2, y4] ]
            [ [x3, y1], [x3, y2], [x3, y3], [x3, y4] ]
            [ [x4, y1], [x4, y2], [x4, y3], [x4, y4] ]
        ]
    :param arrs: list, array list
    :return: list
    """
    # check input arrays
    length = None
    for arr in arrs:
        if length is None:
            length = len(arr)
            continue

        if length != len(arr):
            raise "combine2 needs array length must be the same"

    # combine input arrays item by item
    results = None
    for arr in arrs:
        if results is None:
            results = [ [[elm]] for elm in arr ]
        else:
            tmpresults = [[] for i in range(0, length)]
            for i in range(0, length):
                for res in results[i]:
                    for elm in arr:
                        tmpresults[i].append(res+[elm])
            results = tmpresults

    return results
