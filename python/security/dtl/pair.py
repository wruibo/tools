"""
    pair<key, value> structure definition
"""


class Pair:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    @property
    def key(self):
        return self.key

    @key.setter
    def key(self, k):
        self.key = k

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, v):
        self.value = v
