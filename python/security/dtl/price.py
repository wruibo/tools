"""
    price structure for index,stock,bonds
"""


class Price:
    '''
        a price record for index
    '''
    def __init__(self):
        self.time = None # time of price
        self.open = None # open price
        self.close = None # close price
        self.high = None # highest price
        self.low = None # lowest price
        self.volume = None # trade volume
        self.amount = None # trade amount

    def __str__(self):
        return ','.join(self.values(True))

    def __repr__(self):
        return '\n'.join([','.join(self.keys(True)), ','.join(self.values(True))])

    @staticmethod
    def keys(formatted=False):
        # key name of price data
        keys = ["time", "open", "close", "high", "low", "volumn", "amount"]

        # return original key name list
        if not formatted:
            return keys

        # return same width key name list
        formated_keys = []
        for k in keys:
            formated_keys.append(k.center(16, ' '))
        return formated_keys

    def values(self, formatted=False):
        # relate values of price data
        values = [self.time, self.open, self.close, self.high, self.low, self.volume, self.amount]

        # return original value data list
        if not formatted:
            return values

        # return same width value data list
        formated_values = []
        for v in values:
            formated_values.append(str(v).center(16, ' '))
        return formated_values

    def plot(self):
        pass