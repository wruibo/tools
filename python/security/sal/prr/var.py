"""
    VaR-Value at Risk，
"""
import utl
from . import profit


def all(mtx, datecol, navcol):
    """
        compute all value at risk
    :param mtx:
    :param datecol:
    :param navcol:
    :return:
    """
    vars = var(mtx, datecol, navcol, 100, utl.date.date)
    results = {
        "Day-VaR-1": vars[1],
        "Day-VaR-5": vars[5]
    }

    return results


def var(mtx, datecol, navcol, cirange=100, sample_period_cls=utl.date.date, interp_func=None):
    """
        compute value at risk for input asset
    :param mtx: matrix, nav(price) data
    :param datecol: int, date column number
    :param navcol: int, nav(price) column number
    :param cirange: int, confidence interval range, generally used 100
    :param sample_period_cls: class, class of date/week/month/year/...
    :param interp_func: function, interpolation function
    :return: array
    """
    try:
        # interpolate nav based on the date column
        if interp_func is not None:
            mtx, datecol, navcol = interp_func(mtx, datecol, 1, datecol, navcol), 1, 2

        # return rates for specified period
        profits = list(profit.rolling(mtx, datecol, navcol, sample_period_cls).values())

        # sort profits by descend order
        profits.sort()

        # all confidence interval from range(1, cirange)/cifrange
        ciprofits = []
        step = len(profits) / cirange
        for i in range(0, cirange):
            ciprofits.append(profits[int(i*step)])
        ciprofits.append(profits[-1])

        return ciprofits
    except Exception as e:
        raise e
        #return None
