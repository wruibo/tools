"""
    stock data
"""


class vendor:
    """
        site vendor for loading stock data
    """
    class cninfo:
        @staticmethod
        def name():
            return "cninfo"

        @staticmethod
        def loader():
            from . import cninfo
            return cninfo.loader


# current source vendor for fund data
_vendor = vendor.cninfo


def source(vdr=None):
    """
        choose a source for loading fund's data
    :param vdr: str, specified vendor source
    :return: str, for current source vendor or None
    """
    global _vendor
    if vdr is None:
        return _vendor.loader()

    # change current vendor
    _vendor = vdr


def all(market, code):
    """
        get all fund data for specified fund by its code
    :param code: str, fund code in source
    :return: loader
    """
    return source()(market, code)


class finance:
    """
        finance relate data
    """
    @staticmethod
    def income(market, code, start_year=None, end_year=None):
        return all(market, code).finance_income(start_year, end_year)


    @staticmethod
    def balance(market, code, start_year=None, end_year=None):
        return all(market, code).finance_balance(start_year, end_year)


    @staticmethod
    def cashflow(market, code, start_year=None, end_year=None):
        return all(market, code).finance_cashflow(start_year, end_year)


class quotation:
    """
        quotation data
    """
    @staticmethod
    def daily(market, code, start_year=None, end_year=None):
        return all(market, code).quotation_daily(start_year, end_year)
