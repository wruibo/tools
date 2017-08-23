"""
    fund data management
"""


class vendor:
    """
        site vendor for loading fund's data
    """
    class smpp:
        @staticmethod
        def name():
            return "smpp"

        @staticmethod
        def loader():
            import dbm.fund.simuwang
            return dbm.fund.simuwang.loader

    class ttjj:
        @staticmethod
        def name():
            return "ttjj"

        @staticmethod
        def loader():
            pass

    class cfq:
        @staticmethod
        def name():
            return "cfq"

        @staticmethod
        def loader():
            import dbm.fund.caifuqiao
            return dbm.fund.caifuqiao.loader


# current source vendor for fund data
_vendor = vendor.cfq


def source(vdr=None):
    """
        choose a source for loading fund's data
    :param vdr: str, specified vendor source
    :return: str, for current source vendor or None
    """
    global _vendor
    if vdr is None:
        return _vendor.loader()

    # change current vendor
    _vendor = vdr


def all(code):
    """
        get all fund data for specified fund by its code
    :param code: str, fund code in source
    :return: loader
    """
    return source()(code)


def nav(code):
    """
        get net-asset-value list from data source, return data format:
          [
                [date, nav, aav],
                [date, nav, aav],
                [...]
          ]
    :param code: str, fund's code at data source
    :return: list
    """
    return all(code).nav()


if __name__ == "__main__":
    nav1= nav("1000502")
    print(nav1)
