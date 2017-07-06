"""
    fund class
"""


class Fund:
    def __init__(self, code, name, navs=[]):
        self.code = code # fund code
        self.name = name # fund name
        self.navs = navs # net asset value daily record: date, net-asset-value, acc-net-asset-value

    def navs(self, *navs):
        if len(navs)==0:
            return self.navs

        self.navs = navs

    def __str__(self):
        fund = 'code: %s, name: %s\n' % (self.code, self.name)
        navs = []
        for date, nav, aav in self.navs:
            navs.append('%s, %s, %s\n' % (date, str(nav), str(aav)))

        return '%s\n%s' % (fund, ''.join(navs))

    def __repr__(self):
        return self.__str__()