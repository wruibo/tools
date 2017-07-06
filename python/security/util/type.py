"""
    type converter
"""


def convert(objs, t):
    """
        convert objs's values to type @t
    :param objs: objects, tuple, list, dict
    :param t: to type
    :return:
    """
    if isinstance(objs, tuple):
        lst = []
        for obj in objs:
            lst.append(convert(obj, t))
        return tuple(lst)
    elif isinstance(objs, list):
        lst = []
        for obj in objs:
            lst.append(convert(obj, t))
        return lst
    elif isinstance(objs, dict):
        dct = {}
        for key, value in objs:
            dct[key] = convert(value, t)
        return dct
    else:
        return t(objs)


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
