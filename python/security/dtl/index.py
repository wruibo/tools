"""
    index data class
"""
from dtl.price import Price


class Index:
    """
        index with price records
    """
    def __init__(self, code=None, cname=None, ename=None):
        self.code = code # trade code of index
        self.cname = cname # chinese name of index
        self.ename = ename # english name of index
        self.prices = [] # list of price records

    def __str__(self):
        sprices = []
        for price in self.prices:
            sprices.append(str(price))

        return '\n'.join([','.join(Price.keys(True)), '\n'.join(sprices)])

    def __repr__(self):
        return  'code=%s, name=%s, en=%s\n%s' % (self.code, self.cname, self.ename, self.__str__())
