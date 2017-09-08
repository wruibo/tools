"""
    base allocation model
"""
import utl


class Asset:
    def __init__(self, name, prices):
        self._name = name
        self._prices = prices

    @property
    def name(self):
        return self._name

    @property
    def prices(self):
        return self._prices


class AllocationModel:
    """
        allocation model base class
    """
    def __init__(self, assets):
        self._assets = assets

    @property
    def adjust_period(self):
        return self._adjust_period

    @adjust_period.setter
    def adjust_period(self, apcls):
        self._adjust_period = apcls
