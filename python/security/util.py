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
    return (datetime.datetime.strptime(strEndDate, strFormat) - datetime.datetime.strptime(strStartDate, strFormat)).days