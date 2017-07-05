"""
    fund class
"""


class Fund:
    def __init__(self, code, name):
        self._code = code
        self._name = name
        self._navs = []

    def nav(self, date, nav, aav):
        self._navs.append([date, nav, aav])

    def navs(self):
        return self._navs
