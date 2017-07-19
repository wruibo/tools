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

    result.profit = sal.prr.profit.year(fundnavs, 1, 2)

    result.mdd = sal.prr.mdd.max_drawdown(fundnavs, 2)
    result.mdds = sal.prr.mdd.max_drawdown_trends(fundnavs, 2)
    result.beta = sal.prr.beta(fundbmkbvals, 1, 2, 3)
    result.sharpe = sal.prr.sharpe(fundnavs, 1, 2, 3, rfr)
    result.calmar = sal.prr.calmar(fundnavs, 1, 2)
    result.jensen = sal.prr.jensen(fundbmkbvals, 1, 2, 3, rfr)
    result.treynor = sal.prr.treynor(fundbmkbvals, 1, 2, 3, rfr)
    result.information_ratio = sal.prr.inforatio(fundbmkbvals, 1, 2, 3)

    return result


class AnalysisResult:
    """
        analyse result for fund
    """
    def __init__(self, code):
        self.code = code

        self.profit = None

        self.mdd = None
        self.mdds = None
        self.beta = None
        self.sharpe = None
        self.calmar = None
        self.jensen = None
        self.treynor = None
        self.sortino = None
        self.information_ratio = None

    def __str__(self):
        res = {
            "code":self.code,
            "profit":self.profit,
            "mdd":self.mdd[0],
            "mdds":self.mdds,
            "beta":self.beta,
            "sharpe":self.sharpe,
            "calmar":self.calmar,
            "jensen":self.jensen,
            "treynor":self.treynor,
            "sortnio":self.sortino,
            "information ratio":self.information_ratio
        }

        return utl.string.prettystr(res, 0)

    def __repr__(self):
        return self.__str__()
