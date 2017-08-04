"""
    portfolio construction algorithm
"""
import math


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
            if isinstance(arr, list) or isinstance(arr, tuple):
                for elmt in arr:
                    result.append(elmt*withval)
            else:
                result = arr*withval

        return result



def subcols(mtx, *nums):
    """
        get specified sub columns by number from matrix
    :param mtx: matrix
    :param nums: tuple with int numbers, start from 1
    :return:  matrix
    """
    cols = []

    for num in nums:
        col = []
        for row in mtx:
            col.append(row[num-1])
        cols.append(col)

    return cols


def subcol(mtx, num):
    """
        get specified sub column by number from atrix
    :param mtx: matrix
    :param num: int, column number
    :return: array
    """
    return subcols(mtx, num)[0]


def simulate(navs, times, stepval=0.2, maxsteps=None):
    """
        simulate portfolio by input navs with invest @times, input navs:
        [v1, v2, v3, ..., vn]
    or
        [[v1, pr1], [v2, pr2], ..., [vn, prn]]
    where
        v[i] is nav, pri is probability

    :param navs: list, nav random sequence
    :param times: int, invest times
    :param stepval: float, return step value
    :return: list, return probability distribution
    """
    # check input nav data
    if not (isinstance(navs, list) or isinstance(navs, tuple)):
        raise "input navs must be array."

    has_probability = None
    for nav in navs:
        if has_probability is None:
            if (isinstance(nav, list) or isinstance(nav, tuple)):
                has_probability = True
            else:
                has_probability = False
            continue
        if has_probability:
            if not ((isinstance(nav, list) or isinstance(nav, tuple)) and len(nav) == 2):
                raise "element of input navs must be (nav, probability) or nav"
        else:
            if not (isinstance(nav, int) or isinstance(nav, float)):
                raise "element of input navs must be (nav, probability) or nav"

    # transfer equal probability nav set to (nav, probability) set
    if not has_probability:
        tmpnavs, pr = [], 1.0/len(navs)
        for nav in navs:
            tmpnavs.append([nav, pr])
        navs = tmpnavs

    # combine after invested times
    combine_result = combines(*[navs for i in range(0, times)])

    # generate nav probability distribution set
    prset, maxnav = [], None
    for row in combine_result:
        for elm in row:
            mnavpr = None
            for navpr in elm:
                if mnavpr is None:
                    mnavpr = navpr
                    continue
                mnavpr = multi(mnavpr, navpr)

            # normalize the probability base on 1
            mnavpr = [mnavpr[0], mnavpr[1]]

            # record the max nav
            if maxnav is None:
                maxnav = mnavpr[0]
            else:
                if mnavpr[0]>maxnav:
                    maxnav = mnavpr[0]

            # add to combine nav probability set
            prset.append(mnavpr)

    # compbine nav probability distribution statistic
    steps = math.ceil(maxnav/stepval)+1
    dists = [[i*stepval, 0.0] for i in range(1, steps+1)]
    for nav, pr in prset:
        pos = math.floor(nav/stepval)
        dists[pos][1] = dists[pos][1] + pr

    # only get the max step nav values
    if maxsteps is not None and maxsteps<steps:
        dists = dists[0:maxsteps]

    return dists, prset


def simulate_to_plot(*funds):
    """
        plot simulate result
    :param funds:
    :return:
    """
    # change the invest times, step value, max steps here
    times, stepval, maxsteps = 5, 0.2, None

    # prepare the plot
    import matplotlib.pyplot as plt
    plt.figure(figsize=(16, 8))
    plt.title("portfolio simulate: invest times(%d), step by(%s), max step(%s)" % (times, str(stepval), str(maxsteps)))
    plt.xlabel("return" )
    plt.ylabel("probability")

    # compute each fund's return probability
    num = 1 # fund number from 1
    for navs in funds:
        result, prset = simulate(navs, times, stepval, maxsteps)
        x, y = subcol(result, 1), subcol(result, 2)
        plt.plot(x, y, label="$Fund%d-%s$" % (num, str(navs)))
        num += 1

    # show the plot
    plt.legend()
    plt.show()


def simulate_to_file(*funds):
    """

    :param navs:
    :return:
    """
    # change the invest times, step value, max steps here
    times, stepval, maxsteps = 5, 0.2, None

    # change the file output directory path
    outdir = "./simulate"

    # create the file output directory
    import os
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # simulate portfolio, write to file
    num = 1
    for navs in funds:
        result, prset = simulate(navs, times, stepval, maxsteps)

        # write return probability distribution to file
        arrres = ["return-floor, return-ceil, probability"]
        for ret, pr in result:
            arrres.append("%f, %f, %f" % (ret-stepval, ret, pr))
        strres = "\n".join(arrres)
        fpath = "%s/fund-return-range-prob%d" % (outdir, num)
        with open(fpath, "w") as f:
            f.write(strres)
            f.close()

        # write original return probability set to file
        arrres = ["return, probability"]
        for ret, pr in prset:
            arrres.append("%f, %f" % (ret, pr))
        strres = "\n".join(arrres)
        fpath = "%s/fund-return-prob%d" % (outdir, num)
        with open(fpath, "w") as f:
            f.write(strres)
            f.close()

        num += 1


if __name__ == "__main__":
    # input founds, A, B, C, ... with equal probability
    fundA = [0.05, 0.2, 1, 3, 3, 3]
    fundB = [0.8, 0.9, 1.1, 1.1, 1.2, 1.4]
    fundC = [0.95, 1, 1, 1, 1, 1.1]

    # input fund D, with specified probability, [nav, probability]
    fundD = [[0.05, 0.2], [1, 0.2], [1, 0.1], [1, 0.2], [1, 0.1], [2.1, 0.2]]

    # simulate result to plot
    simulate_to_plot(fundA, fundB, fundC, fundD)

    # simulate result to file
    #simulate_to_file(fundA, fundB, fundC, fundD)
