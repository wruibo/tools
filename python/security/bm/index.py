'''
    index data class
'''


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

    @staticmethod
    def titles():
        return ["time", "open", "close", "high", "low", "volumn", "amount"]

    def values(self):
        return [self.time, self.open, self.close, self.high, self.low, self.volume, self.amount]

    @staticmethod
    def format_titles():
        titles = []
        for t in Price.titles():
            titles.append(t.center(10, ' '))
        return titles

    def format_values(self):
        values = []
        for v in self.values():
            values.append(str(v).rjust(10, ' '))
        return values

    def __str__(self):
        return ','.join(self.format_values())

    def __repr__(self):
        return '\n'.join([','.join(self.format_titles()), ','.join(self.format_values())])


class Index:
    '''
        index with price records
    '''
    def __init__(self, code=None, cname=None, ename=None):
        self.code = code # trade code of index
        self.cname = cname # chinese name of index
        self.ename = ename # english name of index
        self.prices = [] # list of price records

    def __str__(self):
        sprices = []
        for price in self.prices:
            sprices.append(str(price))

        return '\n'.join([','.join(Price.format_titles()), '\n'.join(sprices)])

    def __repr__(self):
        return  'code=%s, name=%s, en=%s\n%s' % (self.code, self.cname, self.ename, self.__str__())
