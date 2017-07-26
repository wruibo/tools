"""
    treynor ratio from CAMP model, formula;
    AssetsTreynorRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / AssetsBetaFactor
"""

import atl, sal


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
        "interpolate":{
            'daily':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.DAILY),
            'weekly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.WEEKLY),
            'monthly':treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.MONTHLY),
            'quarterly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.QUARTERLY),
            'yearly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.YEARLY),
        },
        "original":{
            'daily': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.DAILY),
            'weekly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.WEEKLY),
            'monthly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.MONTHLY),
            'quarterly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.QUARTERLY),
            'yearly': treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.YEARLY),
        }
    }

    return results


def treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
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
        if interp:
            return _treynor_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval, annualdays)
        return _treynor_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval, annualdays)
    except:
        return None

def _treynor_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute treynor ratio for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # treynor ratio
    return _treynor_without_interpolation(mtx, 1, 2, 3, risk_free_rate, interval, annualdays)



def _treynor_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute treynor ratio for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param risk_free_rate: float, risk free rate of year
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, interval, annualdays).values())
    bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, interval, annualdays).values())

    # compute asset&benchmark expect profit
    astexp = atl.array.avg(astprofits)

    # compute asset beta factor
    astbeta = atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)

    # treynor ratio
    return (astexp - risk_free_rate) / astbeta
