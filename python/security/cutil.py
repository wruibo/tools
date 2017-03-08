'''
    useful utility functions
'''

import datetime, gzip, zlib

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

def DateTimes(strDates, strFormat):
    '''
    make datetime list by input string dates list @strDates using string date format @strFormat
    :param strDates: list, string date list
    :param strFormat: string, date format string of the date in @strDates list
    :return: list, convert result of string list to datetime list
    '''
    if isinstance(strDates, list):
        result = []
        for strDate in strDates:
            result.append(datetime.datetime.strptime(strDate, strFormat))
        return result
    else:
        return datetime.datetime.strptime(strDates, strFormat)

def Decompress(fp, encoding):

    encoding = encoding.lower()

    if encoding == "gzip":
        gz = gzip.GzipFile(fileobj=fp)
        return gz.read()
    elif encoding == "deflate":
        return zlib.decompress(fp.read())
    else:
        raise Exception("compress encoding %s is not supported!" % (encoding))