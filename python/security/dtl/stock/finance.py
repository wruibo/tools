"""
    profit of listed company
"""
from dtl.table import table, field


class revenue(table):
    date = field.date("%Y-%m-%d")
    total = field.float(0.0)
    operating = field.float(0.0)


class expense(table):
    date = field.date("%Y-%m-%d")
    total = field.float(0.0)
    operating = field.float(0.0)


class profit(table):
    date = field.date("%Y-%m-%d")
    total = field.float(0.0)
    operating = field.float(0.0)
    net = field.float(0.0)

