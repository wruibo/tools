"""
    compute sharpe\ ratio with the given revenues list, formula:
        AssetsSharpeRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / StandardDeviation(AssetsRevenues)
    constraint:
        the interval of assets revenue sample interval must be the same as risk free return rate interval,
    normally we can use the year return rate for assets and risk free return

    :param revenues: list, interval revenue rate list, example:
        [0.023, 0.032, 0.04, ...]
    :param rf: float, interval risk free return rate, same interval with @revenues
    :return: float, sharpe ratio fo the assets
"""
from atl import interp, xmath
from sal.prr import ret


class Sharpe:
    def __init__(self, tbl, date_column=1, nav_column=2):
        self._table = tbl # table object for holding input data
        self._date_column = date_column # date column name in table
        self._nav_column = nav_column # net asset value column name in table

    def run(self, risk_free_rate, interpolate=False):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        if interpolate:
            return self.sharpe_with_interpolation(risk_free_rate)

        return self.sharpe_without_interpolation(risk_free_rate)

    def sharpe_without_interpolation(self, risk_free_rate):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # compute year return rate based on the nav
        rates = ret.rate(self._table, self._date_column, self._nav_column)

        # compute the asset excess expect return over the risk free asset return
        er = xmath.avg(rates) - risk_free_rate

        # calculate the asset revenue standard deviation
        sd = xmath.stddev(rates)

        # sharpe ratio
        return er/sd

    def sharpe_with_interpolation(self, risk_free_rate):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # interpolate nav based on the date column
        tbl = interp.linear(self._table, self._date_column, self._nav_column, 1)

        # compute year return rate based on the nav
        rates = ret.rate(tbl, 1, 2)

        # compute the asset excess expect return over the risk free asset return
        er = xmath.avg(rates) - risk_free_rate

        # calculate the asset revenue standard deviation
        sd = xmath.stddev(rates)

        # sharpe ratio
        return er/sd
