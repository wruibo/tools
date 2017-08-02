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
            'day':beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.xday),
            'week': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.xweek),
            'month':beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.xmonth),
            'quarter': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.xquarter),
            'year': beta(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.xyear),
        },
        "original":{
            'day': beta(mtx, datecol, astcol, bmkcol, None, dtl.xday),
            'week': beta(mtx, datecol, astcol, bmkcol, None, dtl.xweek),
            'month': beta(mtx, datecol, astcol, bmkcol, None, dtl.xmonth),
            'quarter': beta(mtx, datecol, astcol, bmkcol, None, dtl.xquarter),
            'year': beta(mtx, datecol, astcol, bmkcol, None, dtl.xyear),
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
            mtx = interpfunc(mtx, datecol, 1, datecol, astcol, bmkcol)

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

        # compute beta factor
        return atl.array.cov(astprofits, bmkprofits) / atl.array.var(bmkprofits)
    except:
        return None

