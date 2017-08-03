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

    sum, num, idx = 0.0, len(arr1), 0
    while idx < num:
        sum += (arr1[idx]-expect_value1)*(arr1[idx]-expect_value2)
        idx += 1

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
            raise "array add array need the same length."

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


def rcombine(*arrs):
    """
        random combine items in the arrays, example:
    input arrays:
            [1, 2, 3, 4], [1, 2, 3, 4]
    output result:
            [
                [ [1, 1], [1, 2], [1, 3], [1, 4] ]
                [ [2, 1], [2, 2], [2, 3], [2, 4] ]
                [ [3, 1], [3, 2], [3, 3], [3, 4] ]
                [ [4, 1], [4, 2], [4, 3], [4, 4] ]
            ]
    :param arrs: list, array list
    :return: list
    """
    # check input arrays
    length = None
    for arr in arrs:
        if length is None:
            length = len(arr)
        else:
            if length != len(arr):
                raise "combine2 needs array length must be the same"

    # combine input arrys item by item
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


def pmrcombine(*arrs):
    """
        probability multiplication with random combine items in the arrays, example:
    input arrays:
            [1, 2, 3, 4], [1, 2, 3, 4]
    output result:
            [
                1, 2, 3, 4,
                2, 4, 6, 8,
                3, 6, 9, 12,
                4, 8, 12, 16
            ]
    :param arrs: list, array list
    :return: list
    """
    # check input arrays
    length = None
    for arr in arrs:
        if length is None:
            length = len(arr)
        else:
            if length != len(arr):
                raise "combine2 needs array length must be the same"

    # combine input arrays item by item
    results = None
    for arr in arrs:
        if results is None:
            results = arr
        else:
            tmpresults = []
            for res in results:
                for elm in arr:
                    tmpresults.append(res*elm)
            results = tmpresults

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


if __name__ == "__main__":
    arr = [i for i in range(1, 4)]
    num = 3

    results = combine(arr, num)
    print(results)
    print(len(results))

    results = permute(arr, num)
    print(results)
    print(len(results))

    navs = [1, 2, 3, 4]

    results = rcombine(*[navs for i in range(0, 2)])
    print(results)
    print("%d, %d, %d" % (len(results), len(results[0]), len(results[0][0])))

    results = pmrcombine(*[navs for i in range(0, 2)])
    print(results)
    print(len(results))
