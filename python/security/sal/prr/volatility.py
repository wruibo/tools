"""
    volatility in finance, which is the degree of variation of price, formula:
        volatility(R) = standard-deviation(R)
"""
import atl


def all(mtx, datecol, navcol):
    """
        compute volatility for specified asset navs
    :param mtx: matrix
    :param datecol: int, date column of input nav data
    :param navcol: int, nav column of input nav data
    :return: float, volatility of relate asset
    """
    pass


def volatility(mtx, datecol, navcol, interpfunc=None):
    """
        compute volatility for specified asset navs
    :param mtx: matrix
    :param datecol: int, date column of input nav data
    :param navcol: int, nav column of input nav data
    :param interpfunc: func, interpolate function
    :return: float, volatility of relate asset
    """
    # interplate the nav if interpolate function is specified
    if interpfunc is not None:
        mtx, datecol, navcol = interpfunc(mtx, datecol, 1, datecol, navcol), 1, 2

    # extract navs from mtx
    arr = atl.matrix.subcol(mtx, navcol)

    return atl.array.stddev(arr)
