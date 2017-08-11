"""
    stock data
"""

from .cninfo import cninfo


class vendor:
    """
        data source vendor for stock data
    """
    default = cninfo()
    cninfo = cninfo()

# default stock data source
_stock_data_source = vendor.default


def source(vdr = None):
    """
        get or set the source for stock data
    :param vdr: obj, vendor of source
    :return: vendor or None
    """
    global _stock_data_source
    if vdr is None:
        return _stock_data_source

    _stock_data_source = vdr


class finance:
    """
        finance data for stock
    """
    profit = source().profit
    asset = source().asset
    cashflow = source().cashflow


class quotation:
    """
        quotation data for stock
    """
    daily = source().quotation_daily

