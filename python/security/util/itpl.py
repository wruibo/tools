"""
    interpolation algorithms
"""
import datetime


def linear(xys, clsx, step):
    """
        linear interpolation for input values @xys:
        [
            [x11, y11, y12, ..., y1N]
            [x21, y22, y22, ..., y2N]
            [...]
        ]
    :param xys: matrix base on row records
    :param clsx: x column class for compute
    :param step: step for interpolation of column x
    :param ys: columns want to be interplated
    :return: matrix with x & ys
    """
    # input must be list of list
    if not isinstance(xys, list):
        return

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
        x10, steps = clsx(x1)-clsx(x0), int((clsx(x1)-clsx(x0))/step) - 1
        for j in range(1, steps+1):
            x= str(clsx(x0)+j*step)
            ys, xx0 = [x], clsx(x)-clsx(x0)
            for k in range(0, len(y0s)):
                y = y0s[k] + ((y1s[k]-y0s[k])/x10) * xx0
                ys.append(y)
            result.append(ys)

        # add current record to result
        result.append(xys[i])

        # rebase the x0, y0s
        x0, y0s = x1, y1s

    return result


class Day:
    def __init__(self, date):
        if isinstance(date, str):
            self._date = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            self._date = date

    @property
    def date(self):
        return self._date

    def __str__(self):
        return self._date.strftime("%Y-%m-%d")

    def __add__(self, days):
        return Day(self._date + datetime.timedelta(days))

    def __sub__(self, day):
        if isinstance(day, int):
            return self._date - datetime.timedelta(day)

        return abs((self._date - day._date).days)

if __name__ == "__main__":
    xys = [["2012-01-01",1],["2012-01-03",3],["2012-01-08",8]]
    result = linear(xys, Day, 1)
    print(result)