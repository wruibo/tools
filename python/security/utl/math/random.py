"""
    random
"""


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
