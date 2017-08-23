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
            'day':inforatio(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.day),
            'week': inforatio(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.week),
            'month':inforatio(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.month),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.quarter),
            'year': inforatio(mtx, datecol, astcol, bmkcol, atl.interp.linear, dtl.time.year),
        },
        "original":{
            'day':inforatio(mtx, datecol, astcol, bmkcol, None, dtl.time.day),
            'week': inforatio(mtx, datecol, astcol, bmkcol, None, dtl.time.week),
            'month':inforatio(mtx, datecol, astcol, bmkcol, None, dtl.time.month),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, None, dtl.time.quarter),
            'year': inforatio(mtx, datecol, astcol, bmkcol, None, dtl.time.year),
        }
    }

    return results


def inforatio(mtx, datecol, astcol, bmkcol, interpfunc=None, periodcls=None):
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
        # interpolate the asset&benchmark values
        if interpfunc is not None:
            mtx, datecol, astcol, bmkcol = interpfunc(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, periodcls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, periodcls).values())

        # excess return compare with benchmark
        erprofits = atl.math.sub(astprofits, bmkprofits)

        # compute information ratio
        return atl.math.avg(erprofits) / atl.math.stddev(erprofits)
    except:
        return None
