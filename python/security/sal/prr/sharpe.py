"""
    compute sharpe\ ratio with the given revenues list, formula:
        AssetsSharpeRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / StandardDeviation(AssetsRevenues)
    constraint:
        the interval of assets revenue sample interval must be the same as risk free return rate interval,
    normally we can use the year return rate for assets and risk free return

    :param revenues: list, interval revenue rate list, example:
        [0.023, 0.032, 0.04, ...]
    :param rf: float, interval risk free return rate, same interval with @revenues
    :return: float, sharpe ratio fo the assets
"""
import atl, sal


def sharpe(mtx, datecol, navcol, risk_free_rate, interp=False):
    """
        compute sharpe ratio, default without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :return: sharpe raito
    """
    if interp:
        return _sharpe_with_interpolation(mtx, datecol, navcol, risk_free_rate)

    return _sharpe_without_interpolation(mtx, datecol, navcol, risk_free_rate)


def _sharpe_with_interpolation(mtx, datecol, navcol, risk_free_rate):
    """
        compute sharpe ratio with interpolation
    :return:
    """
    # interpolate nav based on the date column
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, navcol)

    # shape ratio
    return _sharpe_without_interpolation(mtx, 1, 2, risk_free_rate)


def _sharpe_without_interpolation(mtx, datecol, navcol, risk_free_rate):
    """
        compute sharpe ratio without interpolation
    :return:
    """
    # compute year return rate based on the nav
    rates = sal.prr.profit.step(mtx, datecol, navcol)

    # compute the asset excess expect return over the risk free asset return
    er = atl.array.avg(rates) - risk_free_rate

    # calculate the asset revenue standard deviation
    sd = atl.array.stddev(rates)

    # sharpe ratio
    return er/sd
