"""
    jensen ratio in CAMP model, also call alpha， formula:
    AssetsJensenRatio = AssetsExpectRevenue - [rf + AssetsBetaFactor*(MarketExpectRevenue - RiskFreeReturnRate)]
"""
import atl, sal


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
        "interpolate":{
            'daily':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.DAILY),
            'weekly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.WEEKLY),
            'monthly':jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.MONTHLY),
            'quarterly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.QUARTERLY),
            'yearly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, True, sal.YEARLY),
        },
        "original":{
            'daily': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.DAILY),
            'weekly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.WEEKLY),
            'monthly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.MONTHLY),
            'quarterly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.QUARTERLY),
            'yearly': jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, False, sal.YEARLY),
        }
    }

    return results


def jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
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
        if interp:
            return _jensen_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval, annualdays)
        return _jensen_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval, annualdays)
    except:
        return None


def _jensen_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute jensen ratio of asset, with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    # interpolate on date
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # jensen ratio
    return _jensen_without_interpolation(mtx, 1, 2, 3, risk_free_rate, interval, annualdays)


def _jensen_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute jensen ratio of asset, without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
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
    bmkexp = atl.array.avg(bmkprofits)

    # compute asset beta factor
    astbeta = atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)

    # jensen ratio
    return astexp - (risk_free_rate + astbeta * (bmkexp - risk_free_rate))
