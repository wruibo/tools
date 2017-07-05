"""
    date relate functions
"""
import datetime


def datetimes(dates, format="%Y%m%d"):
    """
    make datetime list by input string dates list @dates using string date format @format
    :param dates: list, string date list
    :param format: string, date format string of the date in @dates list
    :return: list, convert result of string list to datetime list
    """
    if isinstance(dates, list):
        result = []
        for date in dates:
            result.append(datetime.datetime.strptime(date, format))
        return result
    else:
        return datetime.datetime.strptime(dates, format)


def days_between(start_date, end_date, format="%Y%m%d"):
    """
    compute the days between start date and end date
    :param start_date: string, start date sting with @format
    :param end_date: string, end date string with @format
    :param format: string, format of the input start and end date string
    :return: number, days between start date and end date
    """
    return abs((datetime.datetime.strptime(end_date, format) - datetime.datetime.strptime(start_date, format)).days)


def date_before(date, days = None, format="%Y%m%d"):
    """
    get the date before @date with @days
    :param date: string, string format date
    :param days: int, days before @date
    :param format: string, format of @date
    :return: string, string date before @date with @days in @format
    """
    if days is None:
        days = 1

    before = datetime.datetime.strptime(date, format) - datetime.timedelta(days)

    return before.strftime(format)
