"""
    equal weight model
"""
import utl
from .. import prr

import matplotlib.pyplot as plt

from .am import AllocationModel


class EqualWeightModel(AllocationModel):
    def __init__(self, assets, allocate_money=None, allocate_date=None):
        """
        :param assets:
        """
        self._assets = assets
        self._money = allocate_money
        self._date = allocate_date

    def allocate(self):
        """
        :return:
        """


    def backtest(self):
        """
        :return:
        """
        assetnum = len(self._assets)
        pass
