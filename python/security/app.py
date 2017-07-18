"""
    application for security
"""
import dbm, sal

import utl, atl

if __name__ == "__main__":
    astvals = atl.matrix.transpose(atl.matrix.subcols(dbm.fund.nav("HF00001FGP"), 1, 3))
    bmkvals = atl.matrix.transpose(atl.matrix.subcols(dbm.index.price(dbm.index.china.hs300).daily(), 1, 3))
    astbmkvals = atl.matrix.transpose(atl.matrix.subcols(atl.matrix.join(astvals, bmkvals, 1, 1), 1, 2, 4))

    print(astvals)
    print(bmkvals)
    print(astbmkvals)

    print(utl.xtime.timerun(sal.prr.sharpe, astvals, 1, 2, 0.03))
    print(utl.xtime.timerun(sal.prr.calmar, astvals, 1, 2))
    print(utl.xtime.timerun(sal.prr.mdd.max_drawdown, astvals, 2))
    print(utl.xtime.timerun(sal.prr.mdd.max_drawdown_trends, astvals, 2))

    print(utl.xtime.timerun(sal.prr.beta, astbmkvals, 1, 2, 3))
    print(utl.xtime.timerun(sal.prr.inforatio, astbmkvals, 1, 2, 3))
    print(utl.xtime.timerun(sal.prr.jensen, astbmkvals, 1, 2, 3, 0.03))
    print(utl.xtime.timerun(sal.prr.treynor, astbmkvals, 1, 2, 3, 0.03))

    print(utl.xtime.timerun(sal.prr.sharpe, bmkvals, 1, 2, 0.03))
    print(utl.xtime.timerun(sal.prr.mdd.fast_max_drawdown, atl.matrix.subcol(bmkvals, 2)))

