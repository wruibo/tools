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


class Sharpe:
    def __init__(self, **kwargs):
        pass

    def run(self):
        pass
