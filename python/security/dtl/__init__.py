"""
    data template library
"""
__all__ = ["fund", "stock", "xday"]

from .core import xtype
from .core import xtable
from .core import xarray

from . import stock


xperiod = xtype.xperiod
xdate = xtype.xdate
xday = xtype.xday
xweek = xtype.xweek
xmonth = xtype.xmonth
xquarter = xtype.xquarter
xyear = xtype.xyear
xrangeday = xtype.xrangeday


def table(rows=None, cols=None):
    """
        create a table object with specified @data
    :param data:
    :return:
    """
    # construct table with rows data
    if rows is not None:
        return xtable.xtable(rows)

    if cols is not None:
        return xtable.xtable(cols).rotate()

    return xtable.xtable()


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


def dates(objs, format):
    """
        convert @objs's values to @xday values
    :param objs: string or tuple, list, dict with string values
    :param format: date format
    :return:
    """
    import datetime
    return convert(objs, datetime.datetime.strptime, format)


def xdates(objs, format):
    """
        convert @objs's values to @xday values
    :param objs: string or tuple, list, dict with string values
    :param format: date format
    :return:
    """
    return convert(objs, xtype.xdate, format)


def absolutes(objs):
    """

    :param objs:
    :return:
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(negatives(obj))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(negatives(obj))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = negatives(value)
        return dct
    else:
        return abs(objs)


def negatives(objs):
    """

    :param objs:
    :return:
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(negatives(obj))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(negatives(obj))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = negatives(value)
        return dct
    else:
        return -objs

def replace(objs, new, *olds):
    """
        replace specified old values in objects to new value
    :param objs: string or tuple, list, dict with string values
    :param new: object, new value
    :param olds: list or tuple, old value
    :return: objs, replace results
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(replace(obj, new, *olds))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(replace(obj, new, *olds))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = replace(value, new, *olds)
        return dct
    else:
        return new if objs in olds else objs
