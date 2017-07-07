"""
    type extensions and type relate functions
"""
import datetime


def convert(objs, t, *args):
    """
        convert objs's values to type @t
    :param objs: objects, tuple, list, dict
    :param t: to type
    :param args: args to pass to t's init function after obj
    :return:
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(convert(obj, t, *args))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(convert(obj, t, *args))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = convert(value, t, *args)
        return dct
    else:
        return t(objs) if len(args)==0 else t(objs, *args)


def floats(objs):
    """
        convert @objs's values to float values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return convert(objs, float)


def ints(objs):
    """
        convert @objs's values to int values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return convert(objs, int)


def strs(objs):
    """
        convert @objs's values to string values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return convert(objs, str)


def xdays(objs, format):
    """
        convert @objs's values to @xday values
    :param objs: string or tuple, list, dict with string values
    :param format: date format
    :return:
    """
    return convert(objs, XDay, format)


class XDay(object):
    def __init__(self, date, format):
        self._format = format
        if isinstance(date, str):
            self._date = datetime.datetime.strptime(date, format)
        else:
            self._date = date

    @property
    def date(self):
        return self._date

    def __str__(self):
        return self._date.strftime(self._format)

    def __repr__(self):
        return self.__str__()

    def __add__(self, days):
        return XDay(self._date + datetime.timedelta(days), self._format)

    def __sub__(self, day):
        if isinstance(day, int):
            return self._date - datetime.timedelta(day)

        return abs((self._date - day.date).days)