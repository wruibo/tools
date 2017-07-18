"""
    fund data management
"""
__all__ = ["simuwang"]


class source:
    """
        site choice for loading fund's data
    """
    simuwang = "simuwang"


def use(where = source.simuwang):
    """
        choose a source for loading fund's data
    :param where: specified site
    :return:
    """
    if where==source.simuwang:
        import dbm.fund.simuwang
        return dbm.fund.simuwang.loader


def all(code):
    """
        get all fund data for specified fund by its code
    :param code: str, fund code in source
    :return: loader
    """
    return use()(code)


def nav(code):
    return all(code).nav()


if __name__ == "__main__":
    nav1= all("HF00000G86").nav()
    print(nav1)

    print(nav("HF00000G86"))
