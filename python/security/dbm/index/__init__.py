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


class source:
    """
        site choice for loading index's data
    """
    csindex = "csindex"


def use(where = source.csindex):
    """
        choose a source for loading index's data
    :param where: specified site
    :return:
    """
    if where==source.csindex:
        import dbm.index.csindex
        return dbm.index.csindex.loader


def all(code):
    """
        get all data for index by specified index code at source site
    :param code: str, code of index at source site
    :return: loader
    """
    return use()(code)


def price(code):
    """
        get price data for index with code
    :param code: str, code of index
    :return: list, price data
    """
    return use()(code).price


if __name__ == "__main__":
    prices = price(china.shzz).daily()
    print(prices)
