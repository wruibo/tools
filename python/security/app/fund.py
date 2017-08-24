"""
    application for fund
"""
import dbm, sal, dtl, utl


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
    fundnavs = dtl.matrix.transpose(dtl.matrix.subcols(dbm.fund.nav(code), 1, 3))
    # list data [[date, price], ...] for selected benchmark
    bcmkvals = dtl.matrix.transpose(dtl.matrix.subcols(dbm.bcmk.hushen300.daily(), 1, 3))
    # list data [[date, fund-nav, benchmark-price], ... ]
    fundbmkbvals = dtl.matrix.transpose(dtl.matrix.subcols(dtl.matrix.join(fundnavs, bcmkvals, 1, 1), 1, 2, 4))

    result = AnalysisResult(code)

    result.ret = sal.prr.profit.all(fundnavs, 1, 2)

    result.mdd = sal.prr.mdd.all(fundnavs, 1, 2)
    result.beta = sal.prr.beta.all(fundbmkbvals, 1, 2, 3)
    result.sharpe = sal.prr.sharpe.all(fundnavs, 1, 2, rfr)
    result.calmar = sal.prr.calmar.all(fundnavs, 1, 2)
    result.jensen = sal.prr.jensen.all(fundbmkbvals, 1, 2, 3, rfr)
    result.treynor = sal.prr.treynor.all(fundbmkbvals, 1, 2, 3, rfr)
    result.sortino = sal.prr.sortino.all(fundnavs, 1, 2, rfr)
    result.information_ratio = sal.prr.infor.all(fundbmkbvals, 1, 2, 3)
    result.volatility = sal.prr.volatility.all(fundnavs, 1, 2)

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
