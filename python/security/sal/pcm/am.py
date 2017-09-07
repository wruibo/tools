"""
    base allocation model
"""
import utl


class Asset:
    def __init__(self):
        pass


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
