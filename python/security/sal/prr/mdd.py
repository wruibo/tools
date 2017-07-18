"""
    max drawdown for specified column data in matrix
"""
import atl


def slow_max_drawdown(mtx, ncol=None):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """
    arr = atl.matrix.subcol(mtx, ncol) if ncol is not None else mtx

    pmax, vmax, pmin, vmin, drawdown = None, None, None, None, None

    i = j = 0
    while i < len(arr):
        j = i + 1
        while j < len(arr):
            ijdrawdown = (arr[j] - arr[i]) / arr[i]
            if (drawdown is None and ijdrawdown<0.0) or ijdrawdown<drawdown:
                pmax, vmax, pmin, vmin, drawdown = i, arr[i], j, arr[j], ijdrawdown
            j += 1
        i += 1

    return drawdown, pmax, vmax, pmin, vmin


def fast_max_drawdown(mtx, ncol=None):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """
    arr = atl.matrix.subcol(mtx, ncol) if ncol is not None else mtx

    pmax, vmax, pmin, vmin, drawdown = None, None, None, None, None
    ipos, ivalue, jpos, jvalue, ijdrawdown = None, None, None, None, None

    i = j = 0
    while i + 1 < len(arr) and j + 1 < len(arr):
        if arr[i] < arr[i+1]:
            i += 1
            continue
        j = i + 1
        while j + 1 < len(arr):
            if arr[j] < arr[j-1] and arr[j] <= arr[j+1]:
                if ijdrawdown is None or arr[j] < jvalue:
                    ipos, ivalue, jpos, jvalue, ijdrawdown = i, arr[i], j, arr[j], (arr[j] - arr[i]) / arr[i]

                if drawdown is None or ijdrawdown < drawdown:
                    pmax, vmax, pmin, vmin, drawdown = ipos, ivalue, jpos, jvalue, ijdrawdown
            else:
                if arr[j] > arr[i]:
                    i = j
                    ipos, ivalue, jpos, jvalue, ijdrawdown = None, None, None, None, None
                    break
            j += 1

    if i < j < len(arr):
        if ijdrawdown is None or arr[j] < jvalue:
            ipos, ivalue, jpos, jvalue, ijdrawdown = i, arr[i], j, arr[j], (arr[j] - arr[i]) / arr[i]

        if drawdown is None or ijdrawdown < drawdown:
            pmax, vmax, pmin, vmin, drawdown = ipos, ivalue, jpos, jvalue, ijdrawdown

    return drawdown, pmax, vmax, pmin, vmin


def slow_max_drawdown_trends(mtx, ncol=None):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    arr = atl.matrix.subcol(mtx, ncol) if ncol is not None else mtx

    dd, j = [], 0
    while j<len(arr):
        i, maxv = 0, arr[0]
        while i<=j:
            if arr[i]>maxv:
                maxv = arr[i]
            i += 1
        dd.append((maxv-arr[j])/maxv)
        j += 1
    return dd


def fast_max_drawdown_trends(mtx, ncol=None):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    arr = atl.matrix.subcol(mtx, ncol) if ncol is not None else mtx

    dd, j, maxi, maxv = [], 0, 0, arr[0]
    while j<len(arr):
        if arr[j]>maxv:
            maxi = j
            maxv = arr[j]
        dd.append((maxv-arr[j])/maxv)
        j += 1
    return dd


def max_drawdown(mtx, ncol=None):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """

    return fast_max_drawdown(mtx, ncol)


def max_drawdown_trends(mtx, ncol=None):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param mtx: matrix
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    return fast_max_drawdown_trends(mtx, ncol)