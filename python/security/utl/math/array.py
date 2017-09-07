"""
    array class defination
"""


def isarray(obj):
    """
        test if input structure is array
    :param obj: object
    :return: boolean, True if input's type is tuple or list
    """
    if isinstance(obj, list) or isinstance(obj, tuple):
        return True
    return False


def like(arr1, arr2):
    """
        test if 2 array has the same structure and element type, example:
        [1, [1, 2], 3] like [2, [3, 4], 1]

        ['1', [1, 2], '3'] not like [2, ['3', '4'], 1]
        [1, [1, 2], 3] not like [2, 3, 4, 1]
    :param arr1: list
    :param arr2: list
    :return: boolean, True if input array like another
    """
    if arr1.__class__ != arr2.__class__:
        return False

    if isarray(arr1) and isarray(arr2):
        if len(arr1) != len(arr2):
            return False
        for i in range(0, len(arr1)):
            if not like(arr1[i], arr2[i]):
                return False
        return True

    return True


def equal(arr1, arr2):
    """
        test if 2 array is equal
    :param arr1: list
    :param arr2: list
    :return:
    """
    return arr1 == arr2


def similar(arr1, arr2):
    """
            test if 2 array has the same structure, example:
        [1, [1, 2], 3] is similar with [2, [3, 4], 1]
        ['1', [1, 2], '3'] si similar with [2, ['3', '4'], 1]

        [1, [1, 2], 3] not similar with [2, 3, 4, 1]
        ['1', [1, 2], '3'] not similar with [2, '3', '4', 1]
    :param arr1: list
    :param arr2: list
    :return: boolean, True if input array similar with another
    """
    if not isarray(arr1) and not isarray(arr2):
        return True

    if isarray(arr1) and isarray(arr2):
        if len(arr1) != len(arr2):
            return False
        for i in range(0, len(arr1)):
            if not similar(arr1[i], arr2[i]):
                return False
        return True

    return False


def maxval(arr, useabs=False):
    """
        get max value in array
    :param arr: array
    :return:  max value
    """
    maxv = None
    for val in arr:
        if maxv is None:
            maxv = maxval(val, useabs) if isarray(val) else abs(val) if useabs else val
            continue

        cval = maxval(val, useabs) if isarray(val) else abs(val) if useabs else val

        if cval>maxv:
            maxv = cval
    return maxv


def add(arr, withval):
    """
        add array data with specified value or another array
    :param arr: list, which will subtract @withval
    :param withval: list or value, which will be subtract with
    :return: array
    """
    result = []
    if isarray(arr):
        if isarray(withval):
            if not similar(arr, withval):
                raise ValueError("can not add input array with another value.")
            for i in range(0, len(arr)):
                result.append(add(arr[i], withval[i]))
        else:
            for i in range(0, len(arr)):
                result.append(add(arr[i], withval))
    else:
        if isarray(withval):
            for i in range(0, len(withval)):
                result.append(add(arr, withval[i]))
        else:
            result = arr + withval

    return result


def sub(arr, withval):
    """
        sub array data with specified value or another array
    :param arr: list, which will subtract @withval
    :param withval: list or value, which will be subtract with
    :return: array
    """
    result = []
    if isarray(arr):
        if isarray(withval):
            if not similar(arr, withval):
                raise ValueError("can not sub input array with another value.")
            for i in range(0, len(arr)):
                result.append(sub(arr[i], withval[i]))
        else:
            for i in range(0, len(arr)):
                result.append(sub(arr[i], withval))
    else:
        if isarray(withval):
            for i in range(0, len(withval)):
                result.append(sub(arr, withval[i]))
        else:
            result = arr - withval

    return result


def multi(arr, withval):
    """
        multiple data in array with other values
    :param arr: array
    :param withval: array, object or None
    :return: multiple result
    """
    result = []
    if isarray(arr):
        if isarray(withval):
            if not similar(arr, withval):
                raise ValueError("can not multi input array with another value.")
            for i in range(0, len(arr)):
                result.append(multi(arr[i], withval[i]))
        else:
            for i in range(0, len(arr)):
                result.append(multi(arr[i], withval))
    else:
        if isarray(withval):
            for i in range(0, len(withval)):
                result.append(multi(arr, withval[i]))
        else:
            result = arr * withval

    return result


def divide(arr, withval):
    """
        divide data in array with other values
    :param arr: array
    :param withval: array, object or None
    :return: multiple result
    """
    result = []
    if isarray(arr):
        if isarray(withval):
            if not similar(arr, withval):
                raise ValueError("can not divide input array with another value.")
            for i in range(0, len(arr)):
                result.append(divide(arr[i], withval[i]))
        else:
            for i in range(0, len(arr)):
                result.append(divide(arr[i], withval))
    else:
        if isarray(withval):
            for i in range(0, len(withval)):
                result.append(divide(arr, withval[i]))
        else:
            result = arr / withval

    return result


def sum(arr):
    """
        compute sum of data in array
    :param arr: array
    :return: product result
    """
    if not isarray(arr):
        return arr

    result = None
    for item in arr:
        if result is None:
            result = item
        else:
            result += sum(item)
    return result


def product(arr):
    """
        compute product of data in array
    :param arr: array
    :return: product result
    """
    if not isarray(arr):
        return arr

    result = None
    for item in arr:
        if result is None:
            result = item
        else:
            result *= product(item)
    return result


def normalize(arr, referval=None):
    """
        normalize values in array
    :param arr: array
    :param referval: float, reference value for normalization
    :return:
    """
    if referval is None:
        referval = maxval(arr, True)

    newarr = []

    for val in arr:
        if isarray(val):
            newarr.append(normalize(val, referval))
        else:
            newarr.append(val/referval)

    return newarr


def strip(arr):
    """
        change the multi-dimension array @mtx to specified dimension, e.g.:
    input:
        [
            [1, 2, 3],
            [4, 5, 6],
            [[7], [8], [9, 10]]
        ]
    output:
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    :param mtx: list, multi dimension array
    :return: list, one dimension array
    """
    if not (isinstance(arr, list) or isinstance(arr, tuple)):
        return [arr]

    results = []

    for elm in arr:
        if isinstance(arr, list) or isinstance(arr, tuple):
            results.extend(strip(elm))
        else:
            results.append(elm)

    return results

