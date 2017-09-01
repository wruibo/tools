"""
    loader
"""


class Dao:
    """
        base class of loader for load stock data from different source
    """

    @property
    def list(self):
        pass

    @property
    def finance(self):
        pass

    @property
    def quotation(self):
        pass
