"""
    treynor ratio from CAMP model, formula;
    AssetsTreynorRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / AssetsBetaFactor
"""

import atl, sal


def treynor(mtx, datecol, astcol, bmkcol, risk_free_rate, interp=False):
    """
        compute treynor ratio for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param risk_free_rate: float, risk free rate of year
    :return: float, beta factor of asset
    """
    if interp:
        return _treynor_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate)
    return _treynor_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate)


def _treynor_with_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute treynor ratio for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param risk_free_rate: float, risk free rate of year
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # treynor ratio
    return _treynor_without_interpolation(mtx, 1, 2, 3)



def _treynor_without_interpolation(mtx, datecol, astcol, bmkcol, risk_free_rate):
    """
        compute treynor ratio for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param risk_free_rate: float, risk free rate of year
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = sal.prr.profit.step(mtx, datecol, astcol)
    bmkprofits = sal.prr.profit.step(mtx, datecol, bmkcol)

    # compute asset&benchmark expect profit
    astexp = atl.array.avg(astprofits)

    # compute asset beta factor
    astbeta = atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)

    # treynor ratio
    return (astexp - risk_free_rate) / astbeta
