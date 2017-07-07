"""
    application for security
"""
import time




if __name__ == "__main__":
    import dbm.index.loader

    shzz = dbm.index.loader.load("shzz")

    import dtl
    closed_values = dtl.extract(shzz.prices, 3)

    from sal.prr import mdd

    print(timerun(mdd.fast_max_drawdown, closed_values))
    print(timerun(mdd.slow_max_drawdown, closed_values))
    print(timerun(mdd.fast_max_drawdown_trends, closed_values))
    print(timerun(mdd.slow_max_drawdown_trends, closed_values))
