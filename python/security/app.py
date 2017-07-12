"""
    application for security
"""
from util import xtime




if __name__ == "__main__":
    import dbm.index.loader

    shzztbl = dbm.index.prices.daily(dbm.index.china.hs300)

    closed_values = shzztbl.getcol(3)[1:]

    from sal.prr import mdd

    print(xtime.timerun(mdd.fast_max_drawdown, closed_values))
    print(xtime.timerun(mdd.slow_max_drawdown, closed_values))
    print(xtime.timerun(mdd.fast_max_drawdown_trends, closed_values))
    print(xtime.timerun(mdd.slow_max_drawdown_trends, closed_values))

    from sal.prr import sharpe
    print(xtime.timerun(sharpe.Sharpe))