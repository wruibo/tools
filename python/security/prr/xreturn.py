"""
    return for asset
"""
from util import date


def rate(table, date_column_name, date_format, nav_column_name, period=365):
    """
        compute period return rates based on the input table data
    :param table:
    :param date_column_name:
    :param date_format:
    :param nav_column_name:
    :param period:
    :return:
    """
    period_rates, last_date, last_nav = [], None, None
    date_navs = table.cols(date_column_name, nav_column_name)

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
