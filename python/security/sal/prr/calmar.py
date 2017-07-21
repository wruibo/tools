"""
    calmar raito, formula:
    calmar(asset) = expect-asset-return / max-drawdown-asset-return
"""

import sal, atl


def calmar(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :return: calmar raito
    """

    # calculate the max drawdown of asset price
    mdd = sal.prr.mdd.max_drawdown(mtx, navcol)

    # compute year return rate based on the nav
    rates = sal.prr.profit.step(mtx, datecol, navcol)

    # compute the asset excess expect return
    er = atl.array.avg(rates)

    # sharpe ratio
    return er/-mdd[0]