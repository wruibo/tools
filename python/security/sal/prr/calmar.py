"""
    calmar raito, formula:
    calmar(asset) = expect-asset-return / max-drawdown-asset-return
"""

import sal, atl


def calmar(mtx, datecol, navcol, interval=None, annualdays=sal.ANNUAL_DAYS):
    """
        compute calmar ratio
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :param interval: int, sal.YEARLY, sal.QUARTERLY, sal.MONTHLY, sal.WEEKLY, sal.DAILY
    :param annualdays: int, days of 1 year
    :return: calmar raito
    """

    # calculate the max drawdown of asset price
    mdd = sal.prr.mdd.max_drawdown(mtx, navcol)

    # compute year return rate based on the nav
    rates = list(sal.prr.profit.rolling(mtx, datecol, navcol, interval, annualdays).values())

    # compute the asset excess expect return
    er = atl.array.avg(rates)

    # sharpe ratio
    return er/-mdd[0]