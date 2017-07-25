"""
    sortino ratio, formula:
        sortino-ratio = (E(Rp) - rfr)/stdev(Rp')
    which Rp' is:
        { rp | rp in Rp and rp<rfr}

"""
import sal, atl


def sortino(mtx, datecol, navcol, risk_free_rate, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
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
    if interp:
        return _sortino_with_interpolation(mtx, datecol, navcol, risk_free_rate, interval, annualdays)

    return _sortino_without_interpolation(mtx, datecol, navcol, risk_free_rate, interval, annualdays)


def _sortino_with_interpolation(mtx, datecol, navcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute sortino ratio with interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param risk_free_rate: float, risk free rate
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return:
    """
    # interpolate nav based on the date column
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, navcol)

    # shape ratio
    return _sortino_without_interpolation(mtx, 1, 2, risk_free_rate, interval, annualdays)



def _sortino_without_interpolation(mtx, datecol, navcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute sortino ratio without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param risk_free_rate: float, risk free rate
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return:
    """
    # compute year return rate based on the nav
    rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, interval, annualdays).values())

    # return rates which is less than risk free return
    drates = []
    for rate in rates:
        if rate < risk_free_rate: drates.append(rate)

    # compute the asset excess expect return over the risk free asset return
    er = atl.array.avg(rates) - risk_free_rate

    # calculate the asset revenue standard deviation
    sd = atl.array.stddev(drates)

    # sharpe ratio
    return er/sd
