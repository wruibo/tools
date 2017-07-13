"""
    fund data management
"""
__all__ = ["loader", "simuwang"]

import dbm.fund.loader
import dbm.fund.simuwang


class site:
    """
        site choice for loading fund's data
    """
    simuwang = "simuwang"

#default source site
_default_source_site = site.simuwang


def source(where = _default_source_site):
    """
        choose a source for loading fund's data
    :param where: specified site
    :return:
    """
    if where==site.simuwang:
        from dbm.fund import simuwang
        return simuwang.Loader()


def all(code):
    """
        get all data of fund @code
    :param code: fund's code in source site
    :return:
    """
    return source().all(code)


def navs(code):
    """
        get navs of fund @code
    :param code: fund's code in source site
    :return: list of nav, [[date, nav, aav], [date, nav, aav], ...]
    """
    return source().navs(code)


if __name__ == "__main__":
    navs = navs("HF00000G86")
    print(navs)
