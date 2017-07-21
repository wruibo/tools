"""
    date relate functions
"""
import datetime


def date(strdate, format="%Y%m%d"):
    """
        make datetime.date object of input string date with specified format
    :param strdate: str, date string to be format
    :param format: str, format of @strdate
    :return: datetime.date
    """
    # first format input date string to datetime
    dt = datetime.datetime.strptime(strdate, format)

    return datetime.date(dt.year, dt.month, dt.day)


def dates(strdates, format="%Y%m%d"):
    """
        make datetime list by input string dates list @strdates using string date format @format
    :param strdates: list, string date list
    :param format: string, date format string of the date in @strdates list
    :return: list, convert result of string list to datetime list
    """
    if isinstance(strdates, list):
        result = []
        for str in strdates:
            result.append(date(str, format))
        return result
    else:
        return date(strdates, format)


def days_between(start_date, end_date, format="%Y%m%d"):
    """
        compute the days between start date and end date
    :param start_date: string, start date sting with @format
    :param end_date: string, end date string with @format
    :param format: string, format of the input start and end date string
    :return: number, days between start date and end date
    """
    return abs((date(end_date, format) - date(start_date, format)).days)


def date_before(strdate, days = None, format="%Y%m%d"):
    """
        get the date before @strdate with @days
    :param strdate: string, string format date
    :param days: int, days before @date
    :param format: string, format of @date
    :return: string, string date before @date with @days in @format
    """
    if days is None:
        days = 1

    before = date(strdate, format) - datetime.timedelta(days)

    return before.strftime(format)


def dates_between(start_date, end_date, format="%Y%m%d"):
    """
        get dates between(and include) specified start date and end date, return results as list
    :param start_date: str, start date
    :param end_date: str, end date
    :param format: str, date string format
    :return: list
    """
    # format string date to date object
    startdt, enddt, reverse = date(start_date, format), date(end_date, format), False
    if startdt > enddt: startdt, enddt, reverse = enddt, startdt, True

    # dates between start and end date
    dates, curdate = [], startdt
    while curdate <= enddt:
        dates.append(curdate)
        curdate = curdate + datetime.timedelta(1)

    if reverse: dates.reverse()

    return dates


def months_between(start_date, end_date, format="%Y%m%d"):
    """
        get months between(and include) specified start date and end date, return results as list
    :param start_date: str, start date
    :param end_date: str, end date
    :param format: str, date string format
    :return: list, month string list
    """
    # format string date to date object
    startdt, enddt, reverse = date(start_date, format), date(end_date, format), False
    if startdt > enddt: startdt, enddt, reverse = enddt, startdt, True

    # get months between start date and end date
    months = []

    # process by different conditions
    if startdt.year == enddt.year:
        syear = str(startdt.year).zfill(4)
        for m in range(startdt.month, enddt.month+1):
            months.append(syear+str(m).zfill(2))
    else:
        # process first year
        ssyear = str(startdt.year).zfill(4)
        for m in range(startdt.month, 13):
            months.append(ssyear + str(m).zfill(2))

        # process medium years
        myear = startdt.year+1
        while myear < enddt.year:
            smyear = str(myear).zfill(4)
            months.extend([smyear+str(m).zfill(2) for m in range(1, 13)])
            myear += 1

        # process last year
        seyear = str(enddt.year).zfill(4)
        for m in range(1, enddt.month + 1):
            months.append(seyear + str(m).zfill(2))

    if reverse: months.reverse()

    return months


def years_between(start_date, end_date, format="%Y%m%d"):
    """
        get years between(and include) specified start date and end date, return results as list
    :param start_date: str, start date
    :param end_date: str, end date
    :param format: str, date string format
    :return: list, year string list
    """
    # format string date to date object
    startdt, enddt, reverse = date(start_date, format), date(end_date, format), False
    if startdt > enddt: startdt, enddt, reverse = enddt, startdt, True

    # get years between start date and end date
    years = []
    for year in range(startdt.year, enddt.year+1):
        years.append(str(year))

    if reverse: years.reverse()

    return years


if __name__ == "__main__":
    import utl.string
    print(date('20170103'))
    print(dates(['20170102', '20180103']))
    print(days_between('20170102', '20170201'))
    print(date_before('20170102'))
    print(utl.string.pretty(dates_between('20170102', '20170203')))
    print(months_between('20150102', '20170908'))
    print(years_between('20010201', '20180103'))
