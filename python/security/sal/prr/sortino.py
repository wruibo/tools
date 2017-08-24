"""
    sortino ratio, formula:
        sortino-ratio = (E(Rp) - rfr)/stdev(Rp')
    which Rp' is:
        { rp | rp in Rp and rp<rfr}

"""
import sal, atl, dtl


def test(mtx, datecol, navcol, risk_free_rate):
    """
        compute all sortino values for portfolio
    :param mtx:
    :param datecol:
    :param navcol:
    :param risk_free_rate:
    :return:
    """
    results = {
        'daily':sortino(mtx, datecol, navcol, risk_free_rate, dtl.time.day, atl.interp.linear),
        'weekly': sortino(mtx, datecol, navcol, risk_free_rate, dtl.time.week, atl.interp.linear),
        'monthly':sortino(mtx, datecol, navcol, risk_free_rate, dtl.time.month, atl.interp.linear),
        'quarterly': sortino(mtx, datecol, navcol, risk_free_rate, dtl.time.quarter, atl.interp.linear),
        'yearly': sortino(mtx, datecol, navcol, risk_free_rate, dtl.time.year, atl.interp.linear)
    }

    return results


def all(mtx, datecol, navcol, risk_free_rate):
    """
        compute all sharpe values for portfolio
    :param mtx:
    :param datecol:
    :param navcol:
    :param risk_free_rate:
    :return:
    """
    results = {
        "total": sortino(mtx, datecol, navcol, risk_free_rate),
        "rolling": {
            "year": rolling(mtx, datecol, navcol, risk_free_rate, dtl.time.year)
        },
        "recent": {
            "year": recent(mtx, datecol, navcol, risk_free_rate, dtl.time.year, [1, 2, 3, 4, 5])
        }
    }

    return results


def sortino(mtx, datecol, navcol, risk_free_rate, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute sortino ratio, default without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param risk_free_rate: float, risk free rate
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: sortino raito
    """
    try:
        # interpolate nav based on the date column
        if interp_func is not None:
            mtx, datecol, navcol = interp_func(mtx, datecol, 1, datecol, navcol), 1, 2

        # compute year return rate based on the nav
        rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, sample_period_cls).values())

        # period compound return rate for specified period
        astexp = sal.prr.profit.compound(mtx, datecol, navcol, sample_period_cls)
        rfrexp = pow((1+risk_free_rate), sample_period_cls.unit_days()/dtl.time.year.unit_days()) - 1.0

        # compute the asset excess expect return over the risk free asset return
        er = astexp- rfrexp


        # return rates which is less than risk free return
        drates = []
        for rate in rates:
            if rate < rfrexp: drates.append(rate)

        # calculate the asset revenue standard deviation
        sd = atl.math.stddev(drates)

        # sortino ratio
        sn = er / sd

        # normalize if wanted
        return sn
    except:
        return None


def rolling(mtx, datecol, astcol, risk_free_rate, rolling_period_cls=dtl.time.year, sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute rolling sharpe ratio
    :param mtx:
    :param datecol:
    :param astcol:
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
            results[prd] = sortino(navs, datecol, astcol, risk_free_rate, sample_period_cls, interp_func)

        return results
    except:
        return None


def recent(mtx, datecol, astcol, risk_free_rate, recent_period_cls=dtl.time.year, periods=[1], sample_period_cls=dtl.time.month, interp_func=None):
    """
        compute recent sharpe ratio
    :param mtx:
    :param datecol:
    :param astcol:
    :param risk_free_rate:
    :param recent_period_cls:
    :param periods:
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
            value = sortino(pmtx, datecol, astcol, risk_free_rate, sample_period_cls, interp_func)

            results[key] = value

        return results
    except:
        return None