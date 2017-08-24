"""
    information ratio, formula:
        IR = (E(PR) - E(BR)) / STDDEV(PR-BR)
    which:
        IR - information ratio of asset or portfolio
        PR - set of portfolio returns, E(PR) means expect PR returns
        BR - set of benchmark returns, E(BR) means expect BR returns
"""
import sal, atl, dtl


def test(mtx, datecol, astcol, bmkcol):
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
            'day':inforatio(mtx, datecol, astcol, bmkcol, dtl.time.day, atl.interp.linear),
            'week': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.week, atl.interp.linear),
            'month':inforatio(mtx, datecol, astcol, bmkcol, dtl.time.month, atl.interp.linear),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.quarter, atl.interp.linear),
            'year': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.year, atl.interp.linear),
        },
        "original":{
            'day':inforatio(mtx, datecol, astcol, bmkcol, dtl.time.day),
            'week': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.week),
            'month':inforatio(mtx, datecol, astcol, bmkcol, dtl.time.month),
            'quarter': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.quarter),
            'year': inforatio(mtx, datecol, astcol, bmkcol, dtl.time.year),
        }
    }

    return results


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
        "total": inforatio(mtx, datecol, astcol, bmkcol),
        "rolling":{
            "year":rolling(mtx, datecol, astcol, bmkcol, dtl.time.year)
        },
        "recent":{
            "year":recent(mtx, datecol, astcol, bmkcol, dtl.time.year, [1, 2, 3, 4, 5])
        }
    }

    return results


def inforatio(mtx, datecol, astcol, bmkcol, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute information ratio for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param sample_period_cls: class, period want to compute information ratio
    :param interp_func: bool, interpolation on date
    :return: float, beta factor of asset
    """
    try:
        # interpolate the asset&benchmark values
        if interp_func is not None:
            mtx, datecol, astcol, bmkcol = interp_func(mtx, datecol, 1, datecol, astcol, bmkcol), 1, 2, 3

        # compute year profit for time revenue
        astprofits = list(sal.prr.profit.rolling(mtx, datecol, astcol, sample_period_cls).values())
        bmkprofits = list(sal.prr.profit.rolling(mtx, datecol, bmkcol, sample_period_cls).values())

        # compound return rate for specified period
        astexp = sal.prr.profit.compound(mtx, datecol, astcol, sample_period_cls)
        bmkexp = sal.prr.profit.compound(mtx, datecol, bmkcol, sample_period_cls)

        # excess return compare with benchmark
        erprofits = atl.math.sub(astprofits, bmkprofits)

        # compute information ratio
        return astexp-bmkexp / atl.math.stddev(erprofits)
    except:
        return None


def rolling(mtx, datecol, astcol, bmkcol, rolling_period_cls=dtl.time.year, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute rolling information ratio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :param rolling_period_cls:
    :param sample_period_cls:
    :param interp_func:
    :return:
    """
    try:
        # split matrix by specified period
        pmtx = dtl.matrix.split(mtx, rolling_period_cls, datecol)

        # compute rolling period beta
        results = {}
        for prd, navs in pmtx.items():
            results[prd] = inforatio(navs, datecol, astcol, bmkcol, sample_period_cls, interp_func)

        return results
    except:
        return None


def recent(mtx, datecol, astcol, bmkcol, recent_period_cls=dtl.time.year, periods=[1], sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute recent information ratio
    :param mtx:
    :param datecol:
    :param astcol:
    :param bmkcol:
    :param rolling_period_cls:
    :param sample_period_cls:
    :param interp_func:
    :return:
    """
    try:
        results = {}
        for period in periods:
            end_date = dtl.time.date.today()
            begin_date = end_date - recent_period_cls.delta(period)
            pmtx = dtl.matrix.select(mtx, lambda x: x>=begin_date, datecol)

            key = dtl.time.daterange(begin_date, end_date)
            value = inforatio(pmtx, datecol, astcol, bmkcol, sample_period_cls, interp_func)

            results[key] = value

        return results
    except:
        return None