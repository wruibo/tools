"""
    information ratio, formula:
        IR = (E(PR) - E(BR)) / STDDEV(PR-BR)
    which:
        IR - information ratio of asset or portfolio
        PR - set of portfolio returns, E(PR) means expect PR returns
        BR - set of benchmark returns, E(BR) means expect BR returns
"""
import sal, atl


def all(mtx, datecol, astcol, bmkcol):
    """
        compute all information ratio values for portfolio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :return:
    """
    results = {
        "interpolate":{
            'daily':inforatio(mtx, datecol, astcol, bmkcol, True, sal.DAILY),
            'weekly': inforatio(mtx, datecol, astcol, bmkcol, True, sal.WEEKLY),
            'monthly':inforatio(mtx, datecol, astcol, bmkcol, True, sal.MONTHLY),
            'quarterly': inforatio(mtx, datecol, astcol, bmkcol, True, sal.QUARTERLY),
            'yearly': inforatio(mtx, datecol, astcol, bmkcol, True, sal.YEARLY),
        },
        "original":{
            'daily': inforatio(mtx, datecol, astcol, bmkcol, False, sal.DAILY),
            'weekly': inforatio(mtx, datecol, astcol, bmkcol, False, sal.WEEKLY),
            'monthly': inforatio(mtx, datecol, astcol, bmkcol, False, sal.MONTHLY),
            'quarterly': inforatio(mtx, datecol, astcol, bmkcol, False, sal.QUARTERLY),
            'yearly': inforatio(mtx, datecol, astcol, bmkcol, False, sal.YEARLY),
        }
    }

    return results


def inforatio(mtx, datecol, astcol, bmkcol, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
    """
        compute information ratio for asset
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
            return _inforatio_with_interpolation(mtx, datecol, astcol, bmkcol, interval, annualdays)
        return _inforatio_without_interpolation(mtx, datecol, astcol, bmkcol, interval, annualdays)
    except:
        return None

def _inforatio_with_interpolation(mtx, datecol, astcol, bmkcol, interval=None, annualdays=None):
    """
        compute information ratio for asset with interpolation on date
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
    return _inforatio_without_interpolation(mtx, 1, 2, 3, interval, annualdays)



def _inforatio_without_interpolation(mtx, datecol, astcol, bmkcol, interval=None, annualdays=None):
    """
        compute information ratio for asset without interpolation on date
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

    # excess return compare with benchmark
    erprofits = atl.array.sub(astprofits, bmkprofits)

    # compute information ratio
    return atl.array.avg(erprofits) / atl.array.stddev(erprofits)
