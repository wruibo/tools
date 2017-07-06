"""
    net value data structure
"""


class Nav:
    def __init__(self):
        self.date = None # net value date
        self.nav = None # net asset value
        self.aav = None # accumulative asset value

    def __str__(self):
        return ','.join(self.values(True))

    def __repr__(self):
        return '\n'.join([','.join(self.keys(True)), ','.join(self.values(True))])

    @staticmethod
    def keys(formatted=False):
        # key name of net asset value data
        keys = ["date", "nav", "aav"]

        # return original key name list
        if not formatted:
            return keys

        # return same width key name list
        formatted_keys = []
        for k in keys:
            formatted_keys.append(k.center(10, ' '))
        return formatted_keys

    def values(self, formatted=False):
        # relate values of price data
        values = [self.date, self.nav, self.aav]

        # return original value data list
        if not formatted:
            return values

        # return same width value data list
        formatted_values = []
        for v in values:
            formatted_values.append(str(v).center(10, ' '))
        return formatted_values

    def plot(self):
        pass
