"""
    beta factor in CAMP model, formula:
       AssetsBetaFactor = Cov(AssetsRevenues, MarketRevenues)/Variance(MarketRevenues)
"""
import atl, dtl, sal


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
            'day':beta(mtx, datecol, astcol, bmkcol, True, dtl.xday),
            'week': beta(mtx, datecol, astcol, bmkcol, True, dtl.xweek),
            'month':beta(mtx, datecol, astcol, bmkcol, True, dtl.xmonth),
            'quarter': beta(mtx, datecol, astcol, bmkcol, True, dtl.xquarter),
            'year': beta(mtx, datecol, astcol, bmkcol, True, dtl.xyear),
        },
        "original":{
            'day': beta(mtx, datecol, astcol, bmkcol, False, dtl.xday),
            'week': beta(mtx, datecol, astcol, bmkcol, False, dtl.xweek),
            'month': beta(mtx, datecol, astcol, bmkcol, False, dtl.xmonth),
            'quarter': beta(mtx, datecol, astcol, bmkcol, False, dtl.xquarter),
            'year': beta(mtx, datecol, astcol, bmkcol, False, dtl.xyear),
        }
    }

    return results


def beta(mtx, datecol, astcol, bmkcol, interp=False, periodcls=None, annualdays=None):
    """
        compute beta factor for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param periodcls: class, period want to compute beta factor
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    try:
        if interp:
            return _beta_with_interpolation(mtx, datecol, astcol, bmkcol, periodcls, annualdays)
        return _beta_without_interpolation(mtx, datecol, astcol, bmkcol, periodcls, annualdays)
    except:
        None

def _beta_with_interpolation(mtx, datecol, astcol, bmkcol, periodcls, annualdays):
    """
        compute beta factor for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param periodcls: class, period want to compute beta factor
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # compute beta factor
    return _beta_without_interpolation(mtx, 1, 2, 3, periodcls, annualdays)



def _beta_without_interpolation(mtx, datecol, astcol, bmkcol, periodcls, annualdays):
    """
        compute beta factor for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param periodcls: class, period want to compute beta factor
    :param annualdays: int, days of 1 year
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls, annualdays).values())
    bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls, annualdays).values())

    # compute beta factor
    return atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)
