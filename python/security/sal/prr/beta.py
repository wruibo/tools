"""
    beta factor in CAMP model, formula:
       AssetsBetaFactor = Cov(AssetsRevenues, MarketRevenues)/Variance(MarketRevenues)
"""
import atl, sal


def beta(mtx, datecol, astcol, bmkcol, interp=False):
    """
        compute beta factor for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :return: float, beta factor of asset
    """
    if interp:
        return _beta_with_interpolation(mtx, datecol, astcol, bmkcol)
    return _beta_without_interpolation(mtx, datecol, astcol, bmkcol)


def _beta_with_interpolation(mtx, datecol, astcol, bmkcol):
    """
        compute beta factor for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # compute beta factor
    return _beta_without_interpolation(mtx, 1, 2, 3)



def _beta_without_interpolation(mtx, datecol, astcol, bmkcol):
    """
        compute beta factor for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = sal.prr.profit.year(mtx, datecol, astcol)
    bmkprofits = sal.prr.profit.year(mtx, datecol, bmkcol)

    # compute beta factor
    return atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)