"""
    treynor ratio from CAMP model, formula;
    AssetsTreynorRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / AssetsBetaFactor
"""

import atl, sal, dtl


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
        'daily':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.day),
        'weekly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.week),
        'monthly':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.month),
        'quarterly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.quarter),
        'yearly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, atl.interp.linear, dtl.time.year)
    }

    return results


def treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, interpfunc=None, periodcls=None):
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
        if interpfunc is not None:
            mtx, datecol, astcol, bmkcol = interpfunc(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

        # period compound return rate for specified period
        astexp = sal.prr.profit.compound(mtx, datecol, astcol, periodcls)
        rfrexp = pow((1+risk_free_rate), periodcls.unitdays()/dtl.time.year.unitdays()) - 1.0

        # compute asset beta factor
        astbeta = atl.math.cov(astprofits, bmkprofits) / atl.math.var(bmkprofits)

        # treynor ratio
        return (astexp - rfrexp) / astbeta
    except:
        return None
