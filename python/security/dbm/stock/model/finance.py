"""
    financial
"""


class Income:
    def __init__(self):
        self._total_revenue = None

    @property
    def total_revenue(self):
        return self._total_revenue


class Asset:
    pass


class CashFlow:
    pass


class Finance:
    def __init__(self):
        self.income = None
        self._assets = None
        self._cashflow = None
