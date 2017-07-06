"""
    return for asset
"""
from util import mtx, date


def rate(matrix, date_column, date_format, nav_column, period=365):
    """
        compute period return rates based on the input matrix or table data
    :param matrix:
    :param date_column_name:
    :param date_format:
    :param nav_column_name:
    :param period:
    :return:
    """
    period_rates, last_date, last_nav = [], None, None
    date_navs = mtx.rotate(matrix.cols(date_column, nav_column))

    for curr_date, curr_nav in date_navs:
        if last_date is None:
            last_date = curr_date
            last_nav = curr_nav
            continue

        days = date.days_between(last_date, curr_date, date_format)
        rate = (curr_nav-last_nav)/last_nav

        period_rate = rate*period/days
        period_rates.append(period_rate)

    return period_rates
