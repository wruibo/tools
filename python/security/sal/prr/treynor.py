"""
    treynor ratio from CAMP model, formula;
    AssetsTreynorRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / AssetsBetaFactor
"""

import utl

from . import profit


def all(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute all treynor values for portfolio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :return:
    """
    results = {
        'daily':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.math.interp.linear, utl.date.day),
        'weekly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.math.interp.linear, utl.date.week),
        'monthly':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.math.interp.linear, utl.date.month),
        'quarterly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.math.interp.linear, utl.date.quarter),
        'yearly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.math.interp.linear, utl.date.year)
    }

    return results


def all(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute all jensen values for portfolio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :return:
    """
    results = {
        "total": treynor(mtx, datecol, astcol, bmkcol, risk_free_rate),
        "rolling":{
            "year":rolling(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.year)
        },
        "recent":{
            "year":recent(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.year, periods=[1, 2, 3, 4, 5])
        }
    }

    return results


def treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls=utl.date.month, interp_func=None):
    """
        compute treynor ratio for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :param interp: bool, interpolation on date
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    try:
        # interpolate the asset&benchmark values
        if interp_func is not None:
            mtx, datecol, astcol, bmkcol = interp_func(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(profit.rolling(mtx, datecol, astcol, sample_period_cls).values())
        bmkprofits = list(profit.rolling(mtx, datecol, bmkcol, sample_period_cls).values())

        # period compound return rate for specified period
        astexp = profit.compound(mtx, datecol, astcol, sample_period_cls)

        rfrexp = pow((1+risk_free_rate), sample_period_cls.unit_days()/utl.date.year.unit_days()) - 1.0

        # compute asset beta factor
        astbeta = utl.math.stat.cov(astprofits, bmkprofits) / utl.math.stat.var(bmkprofits)

        # treynor ratio
        tr = (astexp - rfrexp) / astbeta

        return tr
    except:
        return None


def rolling(mtx, datecol, astcol, bmkcol, risk_free_rate, rolling_period_cls=utl.date.year, sample_period_cls=utl.date.month, interp_func=None):
    """
        compute rolling information ratio
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
        # split matrix by specified period
        pmtx = utl.math.matrix.split(mtx, rolling_period_cls, datecol)

        # compute rolling period beta
        results = {}
        for prd, navs in pmtx.items():
            results[prd] = treynor(navs, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls, interp_func)

        return results
    except:
        return None


def recent(mtx, datecol, astcol, bmkcol, risk_free_rate, recent_period_cls=utl.date.year, periods=[1], sample_period_cls=utl.date.month, interp_func=None):
    """
        compute recent jensen ratio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :param risk_free_rate:
    :param recent_period_cls:
    :param periods:
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
            value = treynor(pmtx, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls, interp_func)

            results[key] = value

        return results
    except:
        return None