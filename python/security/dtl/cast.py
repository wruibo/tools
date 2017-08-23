"""
    object cast
"""


def cast(objs, t, *args):
    """
        cast objs's values to type @t
    :param objs: objects, tuple, list, dict
    :param t: to type
    :param args: args to pass to t's init function after obj
    :return:
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(cast(obj, t, *args))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(cast(obj, t, *args))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = cast(value, t, *args)
        return dct
    else:
        return t(objs) if len(args)==0 else t(objs, *args)


def floats(objs):
    """
        cast @objs's values to float values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return cast(objs, float)


def ints(objs):
    """
        cast @objs's values to int values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return cast(objs, int)


def strs(objs):
    """
        cast @objs's values to string values
    :param objs: objects, tuple, list, dict
    :return:
    """
    return cast(objs, str)


def dates(objs, format):
    """
        cast @objs's values to @xday values
    :param objs: string or tuple, list, dict with string values
    :param format: date format
    :return:
    """
    import datetime
    return cast(objs, datetime.datetime.strptime, format)


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

