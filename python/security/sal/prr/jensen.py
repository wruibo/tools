"""
    jensen ratio in CAMP model, also call alpha， formula:
    AssetsJensenRatio = AssetsExpectRevenue - [rf + AssetsBetaFactor*(MarketExpectRevenue - RiskFreeReturnRate)]
"""
import utl

from . import profit

def test(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute all jensen values for portfolio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :return:
    """
    results = {
        'daily':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.day, utl.math.interp.linear),
        'weekly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.week, utl.math.interp.linear),
        'monthly':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.month, utl.math.interp.linear),
        'quarterly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.quarter, utl.math.interp.linear),
        'yearly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.year, utl.math.interp.linear),
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
        "total": jensen(mtx, datecol, astcol, bmkcol, risk_free_rate),
        "rolling":{
            "year":rolling(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.year)
        },
        "recent":{
            "year":recent(mtx, datecol, astcol, bmkcol, risk_free_rate, utl.date.year, periods=[1, 2, 3, 4, 5])
        }
    }

    return results


def jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls=utl.date.month, interp_func=None, annualize=True):
    """
        compute jensen ratio of asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :param sample_period_cls: int, Day, Week, Month, Quarter, Year
    :param interp_func: bool, interpolation on date
    :return: float, beta factor of asset
    """
    try:
        # interpolate on date
        if interp_func is not None:
            mtx, datecol, astcol, bmkcol = interp_func(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(profit.rolling(mtx, datecol, astcol, sample_period_cls).values())
        bmkprofits = list(profit.rolling(mtx, datecol, bmkcol, sample_period_cls).values())

        # compute asset&benchmark expect profit
        astexp = profit.compound(mtx, datecol, astcol, sample_period_cls)
        bmkexp = profit.compound(mtx, datecol, bmkcol, sample_period_cls)

        days = mtx[-1][datecol-1] - mtx[0][datecol-1] + 1

        rfrexp = pow((1+risk_free_rate),  days/utl.date.year.unit_days()) - 1.0

        # compute asset beta factor
        astbeta = utl.math.stat.cov(astprofits, bmkprofits) / utl.math.stat.var(bmkprofits)

        # jensen ratio
        jr = astexp - (rfrexp + astbeta * (bmkexp - rfrexp))

        # annualize jensen if wanted
        jr = pow(1 + jr, sample_period_cls.yearly_units()) - 1 if annualize else jr

        return jr
    except:
        return None


def rolling(mtx, datecol, astcol, bmkcol, risk_free_rate, rolling_period_cls=utl.date.year, sample_period_cls=utl.date.month, interp_func=None, annualize=True):
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
            results[prd] = jensen(navs, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls, interp_func, annualize)

        return results
    except:
        return None


def recent(mtx, datecol, astcol, bmkcol, risk_free_rate, recent_period_cls=utl.date.year, periods=[1], sample_period_cls=utl.date.month, interp_func=None, annualize=True):
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
            pmtx = utl.matrix.stat.select(mtx, lambda x: x>=begin_date, datecol)

            key = utl.date.daterange(begin_date, end_date)
            value = jensen(pmtx, datecol, astcol, bmkcol, risk_free_rate, sample_period_cls, interp_func, annualize)

            results[key] = value

        return results
    except:
        return None
