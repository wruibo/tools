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
from ds import xmath
from prr import xreturn


class Sharpe:
    def __init__(self, table, date_column_name, date_format, nav_column_name, risk_free_rate):
        self._table = table # table object for holding input data
        self._date_column_name = date_column_name # date column name in table
        self._date_format = date_format  # time column type class in table
        self._nav_column_name = nav_column_name # net asset value column name in table
        self._risk_free_rate = risk_free_rate # risk free asset return rate

    def run(self):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # interpolate nav based on the date column
        table = self._table

        # compute year return rate based on the nav
        rates = xreturn.rate(table, self._date_column_name, self._date_format, self._nav_column_name)

        # compute the asset excess expect return over the risk free asset return
        er = xmath.avg(rates) - self._risk_free_rate

        # calculate the asset revenue standard deviation
        sd = xmath.stddev(*table.col(self._nav_column_name).rows())

        # sharpe ratio
        return er/sd
