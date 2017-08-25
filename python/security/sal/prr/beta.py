"""
    beta factor in CAMP model, formula:
       AssetsBetaFactor = Cov(AssetsRevenues, MarketRevenues)/Variance(MarketRevenues)
"""
import atl, dtl, sal


def test(mtx, datecol, astcol, bmkcol):
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
            'day':beta(mtx, datecol, astcol, bmkcol, dtl.time.day, atl.interp.linear),
            'week': beta(mtx, datecol, astcol, bmkcol, dtl.time.week, atl.interp.linear),
            'month':beta(mtx, datecol, astcol, bmkcol, dtl.time.month, atl.interp.linear),
            'quarter': beta(mtx, datecol, astcol, bmkcol, dtl.time.quarter, atl.interp.linear),
            'year': beta(mtx, datecol, astcol, bmkcol, dtl.time.year, atl.interp.linear),
        },
        "original":{
            'day': beta(mtx, datecol, astcol, bmkcol, dtl.time.day, None),
            'week': beta(mtx, datecol, astcol, bmkcol, dtl.time.week, None),
            'month': beta(mtx, datecol, astcol, bmkcol, dtl.time.month, None),
            'quarter': beta(mtx, datecol, astcol, bmkcol, dtl.time.quarter, None),
            'year': beta(mtx, datecol, astcol, bmkcol, dtl.time.year, None),
        }
    }

    return results


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
        "total": beta(mtx, datecol, astcol, bmkcol),
        "rolling": {
            "year":rolling(mtx, datecol, astcol, bmkcol, dtl.time.year, dtl.time.month, atl.interp.linear),
        },

        "recent": {
            "year":recent(mtx, datecol, astcol, bmkcol, dtl.time.year, [1, 2, 3, 4, 5], dtl.time.month, atl.interp.linear)
        }
    }

    return results


def beta(mtx, datecol, astcol, bmkcol, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute beta factor for asset
    :param mtx: matrix
    :param datecol: int, date column number
    :param astcol: int, asset value column number
    :param bmkcol: int, benchmark value column number
    :param sample_period_cls: class, period want to compute beta factor
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

        # compute beta factor
        return atl.math.cov(astprofits, bmkprofits) / atl.math.var(bmkprofits)
    except:
        return None


def rolling(mtx, datecol, astcol, bmkcol, rolling_period_cls=dtl.time.year, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute rolling beta factor
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
            results[prd] = beta(navs, datecol, astcol, bmkcol, sample_period_cls, interp_func)

        return results
    except:
        return None


def recent(mtx, datecol, astcol, bmkcol, recent_period_cls=dtl.time.year, periods=[1], sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute recent beta factor
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
            value = beta(pmtx, datecol, astcol, bmkcol, sample_period_cls, interp_func)

            results[key] = value

        return results
    except:
        return None
