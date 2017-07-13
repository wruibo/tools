"""
    return for asset
"""
from utl import xmatrix, xdate


def rate(table, date_column, nav_column, period=365):
    """
        compute period return rates based on the input table data
    :param table:
    :param date_column:
    :param nav_column:
    :param period:
    :return:
    """
    period_rates, last_date, last_nav = [], None, None
    date_navs = table.rows(date_column, nav_column)

    for curr_date, curr_nav in date_navs:
        if last_date is None:
            last_date = curr_date
            last_nav = curr_nav
            continue

        days = curr_date-last_date
        rate = (curr_nav-last_nav)/last_nav

        period_rate = rate*period/days
        period_rates.append(period_rate)

    return period_rates
