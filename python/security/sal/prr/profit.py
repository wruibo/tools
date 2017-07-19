"""
    return for asset
"""


def total(mtx, navcol):
    """
        compute total profit
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :return: float, total profix
    """
    return (mtx[-1][navcol-1]-mtx[0][navcol-1]) / mtx[0][navcol-1]


def roll(mtx, datecol, navcol):
    pass


def step(mtx, datecol, navcol, base=None):
    """
        compute step return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param base: int, base period for profit, default yearly
    :return: array, rate array
    """
    period_rates, last_date, last_nav = [], None, None

    for row in mtx:
        curr_date, curr_nav = row[datecol-1], row[navcol-1]
        if last_date is None:
            last_date = curr_date
            last_nav = curr_nav
            continue

        days = curr_date-last_date
        rate = (curr_nav-last_nav)/last_nav

        period_rate = rate*base/days if base is not None else rate/days
        period_rates.append(period_rate)

    return period_rates
