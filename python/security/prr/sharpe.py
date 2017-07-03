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
from ds import type


class Sharpe:
    def __init__(self, table, time_column_name="date", time_column_cls=type.Day, risk_free_rate_column_name="rfr", *nav_column_names):
        self._table = table # table object for holding input data
        self._time_column_name = time_column_name # time column name in table
        self._time_column_cls = time_column_cls  # time column type class in table
        self._risk_free_rate_column_name = risk_free_rate_column_name # risk free rate column name in table
        self._nav_column_names = nav_column_names # net asset value column name in table

    def run(self):
        """
            compute sharpe ratio for each portfolios
        :return:
        """
        # make the interpolation columns
        interpolation_columns = [self._risk_free_rate_column_name]
        interpolation_columns.extend(self._nav_column_names)

        # interpolate nav based on the date column
        table = xmath.linear_interpolation(self._table, self._time_column_name, self._time_column_cls, interpolation_columns)




