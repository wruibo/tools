"""
    time relate functions
"""
import time

def timerun(func, *args, **kwargs):
    """
        run @func with time consume record
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    stime = time.time()
    ret = func(*args, **kwargs)
    etime = time.time()

    return func.__name__, etime-stime, ret