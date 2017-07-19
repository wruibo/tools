"""
    string methods
"""

def prettystr(objs, level=0):
    """
        pretty format an object to string
    :param obj: object, any object
    :return: str
    """
    FILLCH = "\t"

    pstr = ""

    if isinstance(objs, list):
        pstr += lfill("[\n", FILLCH, level)
        for obj in objs:
            pstr += prettystr(obj, level+1)
        pstr += lfill("]\n", FILLCH, level)
    elif isinstance(objs, tuple):
        pstr += lfill("(\n", FILLCH, level)
        for obj in objs:
            pstr += prettystr(obj, level+1)
        pstr += lfill(")\n", FILLCH, level)
    elif isinstance(objs, dict):
        pstr += lfill("{\n", FILLCH, level)
        for key, obj in objs.items():
            pstr += lfill(str(key), FILLCH, level+1)
            pstr += ":\n"
            pstr += prettystr(obj, level+2)
        pstr += lfill("}\n", FILLCH, level)
    else:
        return "%s\n" % lfill(str(objs), FILLCH, level)

    return pstr


def rfill(str, ch, num):
    """
        fill string's right place with character
    :param str: str, string to add right character to
    :param ch: str, character to add to string's right place
    :param num: int, number of @ch to add
    :return: str
    """
    postfix = "".join([ch for i in range(0, num)])

    return "%s%s" % (str, postfix)


def lfill(str, ch, num):
    """
        fill string's left place with character
    :param str: str, string to add left character to
    :param ch: str, character to add to string's left place
    :param num: int, number of @ch to add
    :return: str
    """
    prefix = "".join([ch for i in range(0, num)])

    return "%s%s" % (prefix, str)
