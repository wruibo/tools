"""
    application for security
"""
import time


def timerun(func, *args, **kwargs):
    stime = time.time()
    ret = func(*args, **kwargs)
    etime = time.time()
    return etime-stime, ret

if __name__ == "__main__":
    import bm.loader

    shzz = bm.loader.load("shzz")

    import ds
    closed_values = ds.extract(shzz.prices, 3)

    from prr import mdd
    print(timerun(mdd.fast_max_drawdown, closed_values))
    print(timerun(mdd.slow_max_drawdown, closed_values))
    print(timerun(mdd.fast_max_drawdown_trends, closed_values))
    print(timerun(mdd.slow_max_drawdown_trends, closed_values))
