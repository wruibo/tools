"""
    index data management
"""


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


class site:
    """
        site choice for loading index's data
    """
    csindex = "csindex"


#default source site
_default_source_site = site.csindex


def source(where = _default_source_site):
    """
        choose a source for loading index's data
    :param where: specified site
    :return:
    """
    if where==site.csindex:
        from dbm.index import csindex
        return csindex.Loader()


class prices:
    """
        load the index's prices data
    """
    def daily(code):
        """
            get index daily prices of @code
        :param code: index's code in source site
        :return: list of price list, list of price list, [['date', 'open', 'close', 'high', 'low', 'volume', 'amount'], ...]
        """
        return source().daily(code)


if __name__ == "__main__":
    prices = prices.daily(china.shzz)
    print(prices)
