"""
    data template library
"""
__all__ = ["table", "matrix", "price", "xmath"]


def table(rows=None, cols=None):
    """
        create a table object with specified @data
    :param data:
    :return:
    """
    from dtl.core import xtable

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


def xdays(objs, format):
    """
        convert @objs's values to @xday values
    :param objs: string or tuple, list, dict with string values
    :param format: date format
    :return:
    """
    from dtl.core import xtype
    return convert(objs, xtype.xday, format)
