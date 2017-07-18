"""
    jensen ratio in CAMP model, also call alpha， formula:
    AssetsJensenRatio = AssetsExpectRevenue - [rf + AssetsBetaFactor*(MarketExpectRevenue - RiskFreeReturnRate)]
"""
import atl, sal


def jensen(mtx, datecol, astcol, bmkcol, risk_free_rate, interp=False):
    """
        compute jensen ratio of asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :param interp: bool, interpolation on date
    :return: float, beta factor of asset
    """
    if interp:
        return _jensen_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate)
    return _jensen_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate)


def _jensen_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute jensen ratio of asset, with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :return: float, beta factor of asset
    """
    # interpolate on date
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # jensen ratio
    return _jensen_without_interpolation(mtx, 1, 2, 3, risk_free_rate)

def _jensen_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute jensen ratio of asset, without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :return: float, beta factor of asset
    """
    # compute year profit for time revenue
    astprofits = sal.prr.profit.year(mtx, datecol, astcol)
    bmkprofits = sal.prr.profit.year(mtx, datecol, bmkcol)

    # compute asset&benchmark expect profit
    astexp = atl.array.avg(astprofits)
    bmkexp = atl.array.avg(bmkprofits)

    # compute asset beta factor
    astbeta = atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)

    # jensen ratio
    return astexp - (risk_free_rate + astbeta * (bmkexp - risk_free_rate))
