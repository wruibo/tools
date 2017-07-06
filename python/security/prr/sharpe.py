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
from ds import matrix
from prr import xreturn
from util import mtx, itpl, xmath


class Sharpe:
    def __init__(self, m, date_column, date_format, nav_column, risk_free_rate):
        self._matrix = m # table or matrix object for holding input data
        self._date_column = date_column # date column name in table
        self._date_format = date_format  # time column type class in table
        self._nav_column = nav_column # net asset value column name in table
        self._risk_free_rate = risk_free_rate # risk free asset return rate

    def run(self, interpolate=False):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        if interpolate:
            return self.sharpe_with_interpolation()

        return self.sharpe_without_interpolation()

    def sharpe_without_interpolation(self):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # interpolate nav based on the date column
        m = matrix.Matrix().init(cols=self._matrix.cols(self._date_column, self._nav_column))

        # compute year return rate based on the nav
        rates = xreturn.rate(m, 1, self._date_format, 2)

        # compute the asset excess expect return over the risk free asset return
        er = xmath.avg(rates) - self._risk_free_rate

        # calculate the asset revenue standard deviation
        sd = xmath.stddev(m.col(2).rows())

        # sharpe ratio
        return er/sd

    def sharpe_with_interpolation(self):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # interpolate nav based on the date column
        m = itpl.linear(mtx.rotate(self._matrix.cols(self._date_column, self._nav_column)), itpl.Day, 1)
        m = matrix.Matrix().init(rows=m)

        # compute year return rate based on the nav
        rates = xreturn.rate(m, 1, self._date_format, 2)

        # compute the asset excess expect return over the risk free asset return
        er = xmath.avg(rates) - self._risk_free_rate

        # calculate the asset revenue standard deviation
        sd = xmath.stddev(m.col(2).rows())

        # sharpe ratio
        return er/sd
