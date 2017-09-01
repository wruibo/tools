"""
    stock data loader for different sources
"""
from .cninfo import CNInfo as _CNInfo
from .exchange import Exchange as _Exchange


class _Vendor:
    """
        data source vendor for stock data
    """
    default = _CNInfo
    cninfo = _CNInfo
    exchange = _Exchange

vendor = _Vendor


__source_cls = vendor.default


def use(vdr):
    global __source_cls
    __source_cls = vdr


def dao(market, code):
    return __source_cls(market, code)
