"""
    sortino ratio, formula:
        sortino-ratio = (E(Rp) - rfr)/stdev(Rp')
    which Rp' is:
        { rp | rp in Rp and rp<rfr}

"""
import sal, atl, dtl


def all(mtx, datecol, navcol, risk_free_rate):
    """
        compute all sortino values for portfolio
    :param mtx:
    :param datecol:
    :param navcol:
    :param risk_free_rate:
    :return:
    """
    results = {
        'daily':sortino(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.day),
        'weekly': sortino(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.week),
        'monthly':sortino(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.month),
        'quarterly': sortino(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.quarter),
        'yearly': sortino(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.year)
    }

    return results


def sortino(mtx, datecol, navcol, risk_free_rate, interpfunc=None, periodcls=None):
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
        if interpfunc is not None:
            mtx, datecol, navcol = interpfunc(mtx, datecol, 1, datecol, navcol), 1, 2

        # compute year return rate based on the nav
        rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, periodcls).values())

        # period compound return rate for specified period
        astexp = sal.prr.profit.compound(mtx, datecol, navcol, periodcls)
        rfrexp = pow((1+risk_free_rate), periodcls.unitdays()/dtl.time.year.unitdays()) - 1.0

        # compute the asset excess expect return over the risk free asset return
        er = astexp- rfrexp


        # return rates which is less than risk free return
        drates = []
        for rate in rates:
            if rate < rfrexp: drates.append(rate)

        # calculate the asset revenue standard deviation
        sd = atl.math.stddev(drates)

        # sharpe ratio
        return er / sd
    except:
        return None
