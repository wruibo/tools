"""
    calmar raito, formula:
    calmar(asset) = compound-year-expect-asset-return / max-drawdown-asset-return
"""

import sal, atl, dtl


def test(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx:
    :param datecol:
    :param navcol:
    :return:
    """
    results = {
        "entire":calmar(mtx, datecol, navcol)
    }

    return results


def all(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx:
    :param datecol:
    :param navcol:
    :return:
    """
    results = {
        "total": calmar(mtx, datecol, navcol),
        "rolling":{
            "year":rolling(mtx, datecol, navcol, dtl.time.year)
        },
        "recent":{
            "year":recent(mtx, datecol, navcol, dtl.time.year, periods=[1, 2, 3, 4, 5])
        }
    }

    return results


def calmar(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :return: calmar raito
    """
    try:
        # calculate the max drawdown of asset price
        mdd = sal.prr.mdd.max_drawdown(mtx, navcol)

        # compund annual return rates
        compound_annual_return_rates = sal.prr.profit.compound(mtx, datecol, navcol, dtl.time.year)

        # calmar ratio
        return compound_annual_return_rates/-mdd
    except:
        return None


def rolling(mtx, datecol, navcol, rolling_period_cls=dtl.time.year):
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
        pmtx = dtl.matrix.split(mtx, rolling_period_cls, datecol)

        # compute rolling period beta
        results = {}
        for prd, navs in pmtx.items():
            results[prd] = calmar(navs, datecol, navcol)

        return results
    except:
        return None


def recent(mtx, datecol, navcol, recent_period_cls=dtl.time.year, periods=[1]):
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
            end_date = dtl.time.date.today()
            begin_date = end_date - recent_period_cls.delta(period)
            pmtx = dtl.matrix.select(mtx, lambda x: x>=begin_date, datecol)

            key = dtl.time.daterange(begin_date, end_date)
            value = calmar(pmtx, datecol, navcol)

            results[key] = value

        return results
    except:
        return None
