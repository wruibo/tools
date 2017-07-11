"""
    application for security
"""
from util import xtime




if __name__ == "__main__":
    import dbm.index.loader

    shzz = dbm.index.prices.daily(dbm.index.china.hs300)

    import dtl
    closed_values = dtl.extract(shzz.prices, 3)

    from sal.prr import mdd

    print(xtime.timerun(mdd.fast_max_drawdown, closed_values))
    print(xtime.timerun(mdd.slow_max_drawdown, closed_values))
    print(xtime.timerun(mdd.fast_max_drawdown_trends, closed_values))
    print(xtime.timerun(mdd.slow_max_drawdown_trends, closed_values))
