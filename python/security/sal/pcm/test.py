import math


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

def simulate(navs, times, stepval=0.2, maxsteps=500):
    # navs after invested times
    navs_after_invest_times = pmrcombine(*[navs for i in range(0, times)])

    # steps for statistic
    total = len(navs_after_invest_times)
    steps = math.ceil(max(navs_after_invest_times)/stepval)+1

    # statistic for distribution of returns
    dists = [0 for i in range(0, steps)]
    for nav in navs_after_invest_times:
        pos = math.floor(nav/stepval)
        dists[pos] = dists[pos] + 1


    # probability distribution for returns
    results, curstep = [], 0
    for cnt in dists:
        if curstep < maxsteps:
            results.append(cnt/total)
        else:
            break

        curstep += 1

    return results



if __name__ == "__main__":
    # test return sequence
    navsA = [0.05, 0.2, 1, 3, 3, 3]
    navsB = [0.8, 0.9, 1.1, 1.1, 1.2, 1.4]
    navsC = [0.95, 1, 1, 1, 1, 1.1]

    navsAB = divide(add(navsA, navsB), 2)
    navsAC = divide(add(navsA, navsC), 2)
    navsBC = divide(add(navsB, navsC), 2)


    # you can change times for invest, and or value for figure-x-axis
    times, stepval, maxsteps = 9, 0.2, 300

    # get the simulate results by specified invest times and step value for return distribution statistic
    resA = simulate(navsA, times, stepval, maxsteps)
    resB = simulate(navsB, times, stepval, maxsteps)
    resC = simulate(navsC, times, stepval, maxsteps)

    resAB = simulate(navsAB, times, stepval, maxsteps)
    resAC = simulate(navsAC, times, stepval, maxsteps)
    resBC = simulate(navsBC, times, stepval, maxsteps)

    # plot results
    import matplotlib.pyplot as plt

    plt.figure(figsize=(16, 8))
    plt.xlabel("return rates(x*0.2), invest times(%d), step by(%s)" % (times, str(stepval)))
    plt.ylabel("probability rates")
    plt.plot(resA, label="$A%s$"%str(navsA))
    plt.plot(resB, label="$B%s$"%str(navsB))
    plt.plot(resC, label="$C%s$"%str(navsC))
    plt.plot(resAB, label="$AB%s$" % str(navsAB))
    plt.plot(resAC, label="$AC%s$" % str(navsAC))
    plt.plot(resBC, label="$BC%s$" % str(navsBC))

    plt.legend()
    plt.show()
