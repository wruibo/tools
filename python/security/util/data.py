"""
    normal data process methods
"""


def cols2rows(*columns):
    nrows, ncols = None, len(columns)
    for column in columns:
        if nrows is None:
            nrows = len(column)
            continue

        if nrows!=len(column):
            return None

    rows = []
    for i in range(0, nrows):
        cols = []
        for j in range(0, ncols):
            cols.append(columns[j][i])
        rows.append(columns)

    return rows


