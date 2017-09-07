"""
    equal weight model
"""
import utl

from .am import AllocationModel


class EqualWeightModel(AllocationModel):
    def __init__(self, assets):
        """
        :param assets:
        """
        self._assets = assets

    def allocate(self):
        pass

    def backtest(self):
        pass
