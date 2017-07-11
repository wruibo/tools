"""
    interpolation algorithms
"""


def linear(table, base_column, step, *columns):
    """
        linear interpolation for table @columns on @base_column with @step
    :param table: row table
    :param base_column: base column for interpolation
    :param step: step of base column for interpolation
    :param columns: columns to interpolate
    :return: table with interpolated results
    """

    # extract columns want to be interplated
    xys = table.rcols(base_column, *columns)

    # interpolation result
    result = []

    # process all records
    x0, y0s, total = None, None, len(xys)
    for i in range(0, total):
        # start with the first records
        if x0 is None:
            result.append(xys[i])
            x0, y0s = xys[i][0], xys[i][1:]
            continue

        # interpolate values between current value with last
        x1, y1s = xys[i][0], xys[i][1:]

        # total steps need to interpolate
        x10, steps = x1-x0, int((x1-x0)/step) - 1
        for j in range(1, steps+1):
            x= x0+j*step
            ys, xx0 = [x], x-x0
            for k in range(0, len(y0s)):
                y = y0s[k] + ((y1s[k]-y0s[k])/x10) * xx0
                ys.append(y)
            result.append(ys)

        # add current record to result
        result.append(xys[i])

        # rebase the x0, y0s
        x0, y0s = x1, y1s

    return result

if __name__ == "__main__":
    from dtl import table
    from util import xtype
    table = table.RTable([[xtype.XDay("2012-01-01", "%Y-%m-%d"),1],[xtype.XDay("2012-01-03", "%Y-%m-%d"),3],[xtype.XDay("2012-01-08", "%Y-%m-%d"),8]])
    result = linear(table, 1, 1, 2)
    print(result)