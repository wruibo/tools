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
            'day':beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.day),
            'week': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.week),
            'month':beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.month),
            'quarter': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.quarter),
            'year': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.year),
        },
        "original":{
            'day': beta(mtx, datecol, astcol, bmkcol, None, dtl.time.day),
            'week': beta(mtx, datecol, astcol, bmkcol, None, dtl.time.week),
            'month': beta(mtx, datecol, astcol, bmkcol, None, dtl.time.month),
            'quarter': beta(mtx, datecol, astcol, bmkcol, None, dtl.time.quarter),
            'year': beta(mtx, datecol, astcol, bmkcol, None, dtl.time.year),
        }
    }

    return results


def beta(mtx, datecol, astcol, bmkcol, interpfunc=None, periodcls=None):
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
        # interpolate the asset&benchmark values
        if interpfunc is not None:
            mtx, datecol, astcol, bmkcol = interpfunc(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

        # compute beta factor
        return atl.math.cov(astprofits, bmkprofits) / atl.math.var(bmkprofits)
    except:
        return None

