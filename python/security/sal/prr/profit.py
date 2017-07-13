"""
    return for asset
"""


def year(mtx, datecol, navcol):
    """
        compute year return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param period: int, period for date
    :return: array, rate array
    """
    return period(mtx, datecol, navcol, 365)


def period(mtx, datecol, navcol, period):
    """
        compute period return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param period: int, period for date
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

        period_rate = rate*period/days
        period_rates.append(period_rate)

    return period_rates
