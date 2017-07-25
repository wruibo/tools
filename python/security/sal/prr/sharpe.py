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


def sharpe(mtx, datecol, navcol, risk_free_rate, interp=False, interval=None, annualdays=sal.ANNUAL_DAYS):
    """
        compute sharpe ratio, default without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param interp: interpolation flag on date column for nav
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: sharpe raito
    """
    if interp:
        return _sharpe_with_interpolation(mtx, datecol, navcol, risk_free_rate, interval, annualdays)

    return _sharpe_without_interpolation(mtx, datecol, navcol, risk_free_rate, interval, annualdays)


def _sharpe_with_interpolation(mtx, datecol, navcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute sharpe ratio with interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return:
    """
    # interpolate nav based on the date column
    mtx = atl.interp.linear(mtx, datecol, 1, datecol, navcol)

    # shape ratio
    return _sharpe_without_interpolation(mtx, 1, 2, risk_free_rate, interval, annualdays)


def _sharpe_without_interpolation(mtx, datecol, navcol, risk_free_rate, interval=None, annualdays=None):
    """
        compute sharpe ratio without interpolation
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return:
    """
    # compute year return rate based on the nav
    rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, interval, annualdays).values())

    # compute the asset excess expect return over the risk free asset return
    er = atl.array.avg(rates) - risk_free_rate

    # calculate the asset revenue standard deviation
    sd = atl.array.stddev(rates)

    # sharpe ratio
    return er/sd
