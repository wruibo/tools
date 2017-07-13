"""
    application for security
"""
import dbm, sal

import utl

if __name__ == "__main__":
    navs = dbm.fund.navs("HF00000G86")
    print(utl.xtime.timerun(sal.prr.sharpe, navs, 1, 2, 0.03))

