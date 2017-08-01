"""
    information ratio, formula:
        IR = (E(PR) - E(BR)) / STDDEV(PR-BR)
    which:
        IR - information ratio of asset or portfolio
        PR - set of portfolio returns, E(PR) means expect PR returns
        BR - set of benchmark returns, E(BR) means expect BR returns
"""
import sal, atl, dtl


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
            'day':inforatio(mtx, datecol, astcol, bmkcol, True, dtl.xday),
            'week': inforatio(mtx, datecol, astcol, bmkcol, True, dtl.xweek),
            'month':inforatio(mtx, datecol, astcol, bmkcol, True, dtl.xmonth),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, True, dtl.xquarter),
            'year': inforatio(mtx, datecol, astcol, bmkcol, True, dtl.xyear),
        },
        "original":{
            'day':inforatio(mtx, datecol, astcol, bmkcol, False, dtl.xday),
            'week': inforatio(mtx, datecol, astcol, bmkcol, False, dtl.xweek),
            'month':inforatio(mtx, datecol, astcol, bmkcol, False, dtl.xmonth),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, False, dtl.xquarter),
            'year': inforatio(mtx, datecol, astcol, bmkcol, False, dtl.xyear),
        }
    }

    return results


def inforatio(mtx, datecol, astcol, bmkcol, interp=False, periodcls=None):
    """
        compute information ratio for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param periodcls: class, period want to compute information ratio
    :param annualdays: int, days of 1 year

    :return: float, beta factor of asset
    """
    try:
        if interp:
            return _inforatio_with_interpolation(mtx, datecol, astcol, bmkcol, periodcls)
        return _inforatio_without_interpolation(mtx, datecol, astcol, bmkcol, periodcls)
    except:
        return None


def _inforatio_with_interpolation(mtx, datecol, astcol, bmkcol, periodcls):
    """
        compute information ratio for asset with interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param periodcls: class, period want to compute information ratio
    :return: float, beta factor of asset
    """
    # interpolate the asset&benchmark values
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, astcol, bmkcol)

    # compute beta factor
    return _inforatio_without_interpolation(mtx, 1, 2, 3, periodcls)


def _inforatio_without_interpolation(mtx, datecol, astcol, bmkcol, periodcls):
    """
        compute information ratio for asset without interpolation on date
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param interp: bool, interpolation on date
    :param periodcls: class, period want to compute information ratio
    :return: float, beta factor of asset
    """

    # compute year profit for time revenue
    astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
    bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

    # excess return compare with benchmark
    erprofits = atl.array.sub(astprofits, bmkprofits)

    # compute information ratio
    return atl.array.avg(erprofits) / atl.array.stddev(erprofits)
