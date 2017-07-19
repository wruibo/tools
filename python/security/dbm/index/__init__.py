"""
    index data management
"""

class vendor:
    """
        site vendor for loading index's data
    """
    class zzzs:
        @staticmethod
        def name():
            return "zzzs"

        @staticmethod
        def loader():
            import dbm.index.csindex
            return dbm.index.csindex.loader


# current source vendor for index data
_vendor = vendor.zzzs


def source(vdr=None):
    """
        choose a source for loading index's data
    :param vdr: str, specified vendor source
    :return: str, for current source vendor or None
    """
    global _vendor
    if vdr is None:
        return _vendor.loader()

    # change current vendor
    _vendor = vdr



def all(code):
    """
        get all data for index by specified index code at source site
    :param code: str, code of index at source site
    :return: loader
    """
    return source()(code)


def price(code):
    """
        get price data for index with code
    :param code: str, code of index
    :return: list, price data
    """
    return source()(code).price


if __name__ == "__main__":
    class china:
        """
            china securities index code
        """
        shzz = "000001"
        sz50 = "000016"
        hs300 = "000300"
        zz100 = "000903"
        zz200 = "000904"
        zz500 = "000905"
        zz700 = "000907"

    prices = price(china.shzz).daily()
    print(prices)
