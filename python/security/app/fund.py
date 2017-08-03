"""
    application for fund
"""
import dbm, sal, atl, utl


def source(vdr):
    """
        change fund's data source
    :param code: str, data source code
    :return:
    """
    dbm.fund.source(vdr)


def analyse(code, rfr, bmk=dbm.bcmk.hushen300):
    """
        analyse fund specified by its code
    :param code: str, fund's code
    :param rfr: float, risk free return in year
    :param bmk: object, benchmark for analyse
    :return: dict, analyse results
    """

    # list data [[date, nav],...] for specified fund
    fundnavs = atl.matrix.transpose(atl.matrix.subcols(dbm.fund.nav(code), 1, 3))
    # list data [[date, price], ...] for selected benchmark
    bcmkvals = atl.matrix.transpose(atl.matrix.subcols(dbm.bcmk.hushen300.daily(), 1, 3))
    # list data [[date, fund-nav, benchmark-price], ... ]
    fundbmkbvals = atl.matrix.transpose(atl.matrix.subcols(atl.matrix.join(fundnavs, bcmkvals, 1, 1), 1, 2, 4))

    result = AnalysisResult(code)

    result.ret = sal.prr.profitall(fundnavs, 1, 2)

    result.mdd = sal.prr.mddall(fundnavs, 2)
    result.beta = sal.prr.betaall(fundbmkbvals, 1, 2, 3)
    result.sharpe = sal.prr.sharpeall(fundnavs, 1, 2, rfr)
    result.calmar = sal.prr.calmarall(fundnavs, 1, 2)
    result.jensen = sal.prr.jensenall(fundbmkbvals, 1, 2, 3, rfr)
    result.treynor = sal.prr.treynorall(fundbmkbvals, 1, 2, 3, rfr)
    result.sortino = sal.prr.sortinoall(fundnavs, 1, 2, rfr)
    result.information_ratio = sal.prr.inforatioall(fundbmkbvals, 1, 2, 3)
    result.volatility = sal.prr.volatility(fundnavs, 1, 2)

    return result


class AnalysisResult:
    """
        analyse result for fund
    """
    def __init__(self, code):
        self.code = code

        self.ret = None

        self.mdd = None
        self.beta = None
        self.sharpe = None
        self.calmar = None
        self.jensen = None
        self.treynor = None
        self.sortino = None
        self.information_ratio = None
        self.volatility = None

    def __str__(self):
        res = {
            "code":self.code,
            "return":self.ret,
            "mdd":self.mdd,
            "beta":self.beta,
            "sharpe":self.sharpe,
            "calmar":self.calmar,
            "jensen":self.jensen,
            "treynor":self.treynor,
            "sortnio":self.sortino,
            "information ratio":self.information_ratio,
            "volatility": self.volatility
        }

        return utl.string.pretty(res, 0)

    def __repr__(self):
        return self.__str__()
