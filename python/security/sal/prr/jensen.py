"""
    jensen ratio in CAMP model, also call alpha， formula:
    AssetsJensenRatio = AssetsExpectRevenue - [rf + AssetsBetaFactor*(MarketExpectRevenue - RiskFreeReturnRate)]
"""
import atl, sal, dtl


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
        'daily':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.day),
        'weekly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.week),
        'monthly':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.month),
        'quarterly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.quarter),
        'yearly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.year),
    }

    return results


def jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, interpfunc=None, periodcls=None):
    """
        compute jensen ratio of asset
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
        # interpolate on date
        if interpfunc is not None:
            mtx, datecol, astcol, bmkcol = interpfunc(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

        # compute asset&benchmark expect profit
        astexp = sal.prr.profit.compound(mtx, datecol, astcol, periodcls)
        bmkexp = sal.prr.profit.compound(mtx, datecol, bmkcol, periodcls)
        rfrexp = pow((1 + risk_free_rate), periodcls.unitdays() / dtl.time.date.unitdays()) - 1.0

        # compute asset beta factor
        astbeta = atl.math.cov(astprofits, bmkprofits) / atl.math.var(bmkprofits)

        # jensen ratio
        return astexp - (rfrexp + astbeta * (bmkexp - rfrexp))
    except:
        return None

