"""
    max drawdown for specified column data in matrix(or array)
input:
    matrix:
    [
        [x01, x02, ..., x0m],
        [x11, x12, ..., x1m],
        [x21, x22, ..., x2m],
        [       ...        ],
        [xn1, xn2, ..., xnm]
    ]

or
    array:
    [x0, x1, x2, ..., xn]
"""
import utl


def test(mtx, ncol=None):
    """
        compute all max drawdown indicators
    :param mtx: matrix or array
    :param ncol: int or None, which column in matrix want to compute drawdown indicator
    :return: dict
    """

    results = {
        "max-drawdown": max_drawdown(mtx, ncol),
        "trends-drawdown": max_drawdown_trends(mtx, ncol)
    }

    return results


def all(mtx, datecol, ncol):
    """
        compute all max drawdown indicators
    :param mtx: matrix or array
    :param ncol: int or None, which column in matrix want to compute drawdown indicator
    :return: dict
    """

    results = {
        "total": max_drawdown(mtx, ncol),
        "rolling": {
            "year": rolling(mtx, datecol, ncol, utl.date.year)
        },
        "recent": {
            "year": recent(mtx, datecol, ncol, utl.date.year, [1, 2, 3, 4, 5])
        }
    }

    return results


def trend(mtx, ncol=None):
    """
        mdd trend
    :param mtx:
    :param ncol:
    :return:
    """
    return max_drawdown_trends(mtx, ncol)


def slow_max_drawdown(mtx, ncol=None):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """
    arr = utl.math.matrix.subcol(mtx, ncol) if ncol is not None else mtx

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

    return drawdown #, pmax, vmax, pmin, vmin


def fast_max_drawdown(mtx, ncol=None):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """
    arr = utl.math.matrix.subcol(mtx, ncol) if ncol is not None else mtx

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

    return drawdown #, pmax, vmax, pmin, vmin


def slow_max_drawdown_trends(mtx, ncol=None):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    arr = utl.math.matrix.subcol(mtx, ncol) if ncol is not None else mtx

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
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    arr = utl.math.matrix.subcol(mtx, ncol) if ncol is not None else mtx

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
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """

    return fast_max_drawdown(mtx, ncol)


def max_drawdown_trends(mtx, ncol=None):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param mtx: matrix, or array
    :param ncol: int, which column in matrix want to compute
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """
    return fast_max_drawdown_trends(mtx, ncol)


def rolling(mtx, datecol, navcol, rolling_period_cls=utl.date.year):
    """
        compute rolling mdd by specified period
    :param mtx:
    :param datecol:
    :param navcol:
    :param rolling_period_cls:
    :return:
    """
    try:
        # split matrix by specified period
        pmtx = utl.math.matrix.split(mtx, rolling_period_cls, datecol)

        # compute rolling period beta
        results = {}
        for prd, navs in pmtx.items():
            results[prd] = max_drawdown(navs, navcol)

        return results
    except:
        return None


def recent(mtx, datecol, navcol, recent_period_cls=utl.date.year, periods=[1]):
    """
        compute recent mdd by sepcified period
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :param rolling_period_cls:
    :param sample_period_cls:
    :param interp_func:
    :return:
    """
    try:
        results = {}
        for period in periods:
            end_date = utl.date.date.today()
            begin_date = end_date - recent_period_cls.delta(period)
            pmtx = utl.math.matrix.select(mtx, lambda x: x>=begin_date, datecol)

            key = utl.date.daterange(begin_date, end_date)
            value = max_drawdown(pmtx, navcol)

            results[key] = value

        return results
    except:
        return None