"""
    stock models
"""


class Stock:
    """
        stock data
    """
    def __init__(self):
        self._finance=None

    @property
    def finance(self):
        return self._finance

class Statistics:
    pass

class Finance:
    """
        finance data
    """
    def __init__(self):
        self._revenue = None
        self._profit = None
        self._expense = None


class Revenue:
    date = DateField("%Y-%m-%d")
    total = FloatField(0.0)
    operating = FloatField(0.0)


class Expense(Model):
    date = DateField("%Y-%m-%d")
    total = FloatField(0.0)
    operating = FloatField(0.0)


class Profit(Model):
    date = DateField("%Y-%m-%d")
    total = FloatField(0.0)
    operating = FloatField(0.0)
    net = FloatField(0.0)


stock = Stock()

