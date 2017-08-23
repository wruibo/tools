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
import atl, sal, dtl


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
        'daily':sharpe(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.day),
        'weekly': sharpe(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.week),
        'monthly':sharpe(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.month),
        'quarterly': sharpe(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.quarter),
        'yearly': sharpe(mtx, datecol, navcol, risk_free_rate, atl.interp.linear, dtl.time.year)
    }

    return results


def sharpe(mtx, datecol, navcol, risk_free_rate, interpfunc=None, periodcls=None):
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
    try:
        # interpolate nav based on the date column
        if interpfunc is not None:
            mtx, datecol, navcol = interpfunc(mtx, datecol, 1, datecol, navcol), 1, 2

        # return rates for specified period
        rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, periodcls).values())

        # period compound return rate for specified period
        astexp = sal.prr.profit.compound(mtx, datecol, navcol, periodcls)
        rfrexp = pow((1+risk_free_rate), periodcls.unitdays()/dtl.time.year.unitdays()) - 1.0

        # compute the asset excess expect return over the risk free asset return
        er = astexp - rfrexp

        # calculate the asset revenue standard deviation
        sd = atl.math.stddev(rates)

        # sharpe ratio
        return er / sd
    except:
        return None