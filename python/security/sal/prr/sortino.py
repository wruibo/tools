"""
    sortino ratio, formula:
        sortino-ratio = (E(Rp) - rfr)/stdev(Rp')
    which Rp' is:
        { rp | rp in Rp and rp<rfr}

"""
import sal, atl


def sortino(mtx, datecol, navcol, risk_free_rate, interp=False):
    """
        compute sortino ratio, default without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :return: sortino raito
    """
    if interp:
        return _sortino_with_interpolation(mtx, datecol, navcol, risk_free_rate)

    return _sortino_without_interpolation(mtx, datecol, navcol, risk_free_rate)


def _sortino_with_interpolation(mtx, datecol, navcol, risk_free_rate):
    """
        compute sharpe ratio with interpolation
    :return:
    """
    # interpolate nav based on the date column
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, navcol)

    # shape ratio
    return _sortino_without_interpolation(mtx, 1, 2, risk_free_rate)



def _sortino_without_interpolation(mtx, datecol, navcol, risk_free_rate):
    """
        compute sharpe ratio without interpolation
    :return:
    """
    # compute year return rate based on the nav
    rates = sal.prr.profit.step(mtx, datecol, navcol, sal.ANNUAL_DAYS)

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