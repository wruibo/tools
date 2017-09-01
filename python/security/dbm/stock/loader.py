"""
    stock data access object
"""
from . import source as _source


class MarketLoader:
    def __init__(self):
        pass

    def __getattr__(self, item):
        return StockLoader(item)


    @property
    def list(self):
        pass


class StockLoader:
    def __init__(self, market):
        self._market = market

    def __getattr__(self, code):
        return _source.dao(self._market, code)

    @property
    def finance(self):
        pass

    @property
    def quotation(self):
        pass
