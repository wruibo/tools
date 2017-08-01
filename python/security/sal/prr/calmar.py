"""
    calmar raito, formula:
    calmar(asset) = expect-asset-return / max-drawdown-asset-return
"""

import sal, atl, dtl


def all(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx:
    :param datecol:
    :param navcol:
    :return:
    """
    results = {
        "entire":calmar(mtx, datecol, navcol)
    }

    pmtxs = atl.matrix.split(mtx, dtl.xyear, datecol)
    for prd, pmtx in pmtxs.items():
        results[str(prd)] = calmar(pmtx, datecol, navcol)

    return results


def calmar(mtx, datecol, navcol):
    """
        compute calmar ratio
    :param mtx: matrix, nav data
    :param datecol: int, date column
    :param navcol: int, nav column
    :return: calmar raito
    """
    try:
        # calculate the max drawdown of asset price
        mdd = sal.prr.mdd.max_drawdown(mtx, navcol)

        # compund annual return rates
        compound_annual_return_rates = sal.prr.profit.compound(mtx, datecol, navcol, dtl.xyear)

        # calmar ratio
        return compound_annual_return_rates/-mdd[0]
    except:
        return None
