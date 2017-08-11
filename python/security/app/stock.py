import dbm


def source(vdr=None):
    """
        get or set stock data source
    :param vdr: vendor or None
    :return: vendor or None
    """
    if vdr is None:
        return dbm.stock.source()

    dbm.stock.source(vdr)


class market:
    """
        market defination
    """
    shenzhen = 'sz'
    shanghai = 'sh'


def analyse(market, code, starty=None, endy=None):
    """
        analyse stock with @code in @market
    :param market: str, market code for stock
    :param code: str, code of stock
    :param starty: int, start year for data
    :param endy: int, end year for data
    :return:
    """
    results = {
        "profit": dbm.stock.finance.profit(market, code, starty, endy),
        "asset": dbm.stock.finance.asset(market, code, starty, endy),
        "cashflow": dbm.stock.finance.cashflow(market, code, starty, endy),
        "quotation": dbm.stock.quotation.daily(market, code, starty, endy)
    }

    return results


def display(market, code, starty=None, endy=None):
    """
        display analyse result for stock with @code in @market
    :param market: str, market code for stock
    :param code: str, code of stock
    :param starty: int, start year for data
    :param endy: int, end year for data
    :return:
    """


if __name__ == "__main__":
    import app
    results = app.stock.analyse(app.stock.market.shanghai, '601318', 0, 2017)
    for name, items in results.items():
        print(name)
        for row in items:
            print(row)
