"""
    volatility in finance, which is the degree of variation of price, formula:
        volatility(R) = standard-deviation(R)
"""
import utl

from . import profit


def all(mtx, datecol, navcol):
    """
        compute volatility for specified asset navs
    :param mtx: matrix
    :param datecol: int, date column of input nav data
    :param navcol: int, nav column of input nav data
    :return: float, volatility of relate asset
    """
    results = {
        "total": volatility(mtx, datecol, navcol),
        "rolling":{
            "year":rolling(mtx, datecol, navcol, utl.date.year)
        },
        "recent":{
            "year":recent(mtx, datecol, navcol, utl.date.year, periods=[1, 2, 3, 4, 5])
        }
    }

    return results


def volatility(mtx, datecol, navcol, sample_period_cls=utl.date.month, interp_func=None, annualize=True):
    """
        compute volatility for specified asset navs
    :param mtx: matrix
    :param datecol: int, date column of input nav data
    :param navcol: int, nav column of input nav data
    :param interp_func: func, interpolate function
    :return: float, volatility of relate asset
    """
    # interplate the nav if interpolate function is specified
    if interp_func is not None:
        mtx, datecol, navcol = interp_func(mtx, datecol, 1, datecol, navcol), 1, 2

    # profits
    profits = list(profit.rolling(mtx, datecol, navcol, sample_period_cls).values())

    # volatility
    vt = utl.math.stat.stddev(profits)

    # annualize
    vt = vt * pow(sample_period_cls.yearly_units(), 0.5) if annualize else vt

    return vt


def rolling(mtx, datecol, navcol, rolling_period_cls=utl.date.year, sample_period_cls=utl.date.month, interp_func=None, annualize=True):
    """
        compute rolling calmar by specified period
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
            results[prd] = volatility(navs, datecol, navcol, sample_period_cls, interp_func, annualize)

        return results
    except:
        return None


def recent(mtx, datecol, navcol, recent_period_cls=utl.date.year, periods=[1], sample_period_cls=utl.date.month, interp_func=None, annualize=True):
    """
        compute recent beta factor
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
            value = volatility(pmtx, datecol, navcol, sample_period_cls, interp_func, annualize)

            results[key] = value

        return results
    except:
        return None
