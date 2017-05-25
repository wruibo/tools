'''
    timer tools
'''
import time


class ctimer:
    def __init__(self):
        pass

    @staticmethod
    def timerun(func, *args, **kwargs):
        stime = time.time()
        ret = func(*args, **kwargs)
        etime = time.time()

        return etime - stime, ret