"""
    max drawdown for continuous values
"""


def slow_max_drawdown(values):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param values: list, sequence value in list
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """

    if not (isinstance(values, list) or isinstance(values, tuple)):
        return None

    pmax, vmax, pmin, vmin, drawdown = None, None, None, None, None

    i = j = 0
    while i < len(values):
        j = i + 1
        while j < len(values):
            ijdrawdown = (values[j] - values[i]) / values[i]
            if (drawdown is None and ijdrawdown<0.0) or ijdrawdown<drawdown:
                pmax, vmax, pmin, vmin, drawdown = i, values[i], j, values[j], ijdrawdown
            j += 1
        i += 1

    return drawdown, pmax, vmax, pmin, vmin


def fast_max_drawdown(values):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param values: list, sequence value in list
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """

    pmax, vmax, pmin, vmin, drawdown = None, None, None, None, None
    ipos, ivalue, jpos, jvalue, ijdrawdown = None, None, None, None, None

    i = j = 0
    while i + 1 < len(values) and j + 1 < len(values):
        if values[i] < values[i+1]:
            i += 1
            continue
        j = i + 1
        while j + 1 < len(values):
            if values[j] < values[j-1] and values[j] <= values[j+1]:
                if ijdrawdown is None or values[j] < jvalue:
                    ipos, ivalue, jpos, jvalue, ijdrawdown = i, values[i], j, values[j], (values[j] - values[i]) / values[i]

                if drawdown is None or ijdrawdown < drawdown:
                    pmax, vmax, pmin, vmin, drawdown = ipos, ivalue, jpos, jvalue, ijdrawdown
            else:
                if values[j] > values[i]:
                    i = j
                    ipos, ivalue, jpos, jvalue, ijdrawdown = None, None, None, None, None
                    break
            j += 1

    if i < j < len(values):
        if ijdrawdown is None or values[j] < jvalue:
            ipos, ivalue, jpos, jvalue, ijdrawdown = i, values[i], j, values[j], (values[j] - values[i]) / values[i]

        if drawdown is None or ijdrawdown < drawdown:
            pmax, vmax, pmin, vmin, drawdown = ipos, ivalue, jpos, jvalue, ijdrawdown

    return drawdown, pmax, vmax, pmin, vmin


def slow_max_drawdown_trends(values):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param values: list, sequence value in list
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """

    dd, j = [], 0
    while j<len(values):
        i, maxv = 0, values[0]
        while i<=j:
            if values[i]>maxv:
                maxv = values[i]
            i += 1
        dd.append((maxv-values[j])/maxv)
        j += 1
    return dd


def fast_max_drawdown_trends(values):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param values: list, sequence value in list
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """

    dd, j, maxi, maxv = [], 0, 0, values[0]
    while j<len(values):
        if values[j]>maxv:
            maxi = j
            maxv = values[j]
        dd.append((maxv-values[j])/maxv)
        j += 1
    return dd


def max_drawdown(values):
    """
    compute the max drawdown of the given value list, using normal algorithm:
        max drawdown = max{vi-vj/vi}, 0=<i<j<=n
    :param values: list, sequence value in list
    :return: [max-drawdown, pos max, value max, pos min, value min] of the list
    """

    return fast_max_drawdown(values)


def max_drawdown_trends(values):
    """
    compute max drawdown sequence by treat every point as sellout point
    :param values: list, sequence value in list
    :return: list, [max-drawdown0, max-drawdown1, ....]
    """

    return fast_max_drawdown_trends(values)