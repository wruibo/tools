'''
    useful utility functions
'''

import datetime

def DaysBetween(strStartDate, strEndDate, strFormat = "%Y%m%d"):
    '''
    compute the days between start date and end date
    :param strStartDate: string, start date sting with @strFormat
    :param strEndDate: string, end date string with @strFormat
    :param strFormat: string, format of the input start and end date string
    :return: number, days between start date and end date
    '''
    return abs((datetime.datetime.strptime(strEndDate, strFormat) - datetime.datetime.strptime(strStartDate, strFormat)).days)

def DateBefore(strDate, days = None, strFormat = "%Y%m%d"):
    '''
    get the date before @strDate with @days
    :param strDate: string, string format date
    :param days: int, days before @strDate
    :param strFormat: string, format of @strDate
    :return: string, string date before @strDate with @days in @strFormat
    '''
    if days is None:
        days = 1

    before = datetime.datetime.strptime(strDate, strFormat) - datetime.timedelta(days)

    return before.strftime(strFormat)

def ConvertType(container, type):
    '''
    convert the item type in the container to specified type recursively
    :param container: list or Object, whose item will be converted
    :param type: type, type to be convert to
    :return: list or Object, convert result
    '''
    if isinstance(container, list):
        result = []
        for item in container:
            result.append(ConvertType(item, type))
        return result
    else:
        return type(container)