"""
    beta factor in CAMP model, formula:
       AssetsBetaFactor = Cov(AssetsRevenues, MarketRevenues)/Variance(MarketRevenues)
"""
import atl, sal


def all(mtx, datecol, astcol, bmkcol):
    """
        compute all beta values for portfolio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :return:
    """
    results = {
        "interpolate":{
            'daily':beta(mtx, datecol, astcol, bmkcol, True, sal.DAILY),
            'weekly': beta(mtx, datecol, astcol, bmkcol, True, sal.WEEKLY),
            'monthly':beta(mtx, datecol, astcol, bmkcol, True, sal.MONTHLY),
            'quarterly': beta(mtx, datecol, astcol, bmkcol, True, sal.QUARTERLY),
            'yearly': beta(mtx, datecol, astcol, bmkcol, True, sal.YEARLY),
        },
        "original":{
            'daily': beta(mtx, datecol, astcol, bmkcol, False, sal.DAILY),
            'weekly': beta(mtx, datecol, astcol, bmkcol, False, sal.WEEKLY),
            'monthly': beta(mtx, datecol, astcol, bmkcol, False, sal.MONTHLY),
            'quarterly': beta(mtx, datecol, astcol, bmkcol, False, sal.QUARTERLY),
            'yearly': beta(mtx, datecol, astcol, bmkcol, False, sal.YEARLY),
        }
    }

    return results


def beta(mtx, datecol, astcol, bmkcol, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
    """
        compute beta factor for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    try:
        if interp:
            return _beta_with_interpolation(mtx, datecol, astcol, bmkcol, interval, annualdays)
        return _beta_without_interpolation(mtx, datecol, astcol, bmkcol)
    except:
        None

def _beta_with_interpolation(mtx, datecol, astcol, bmkcol, interval=None, annualdays=None):
    """
        compute beta factor for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # compute beta factor
    return _beta_without_interpolation(mtx, 1, 2, 3, interval, annualdays)



def _beta_without_interpolation(mtx, datecol, astcol, bmkcol, interval=None, annualdays=None):
    """
        compute beta factor for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, interval, annualdays).values())
    bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, interval, annualdays).values())

    # compute beta factor
    return atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)
