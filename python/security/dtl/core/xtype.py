"""
    type extensions and type relate functions
"""
import datetime


class xdate(datetime.date):
    """
        extends the datetime.date class
    """
    def __new__(cls, strdate, format="%Y%m%d"):
        # initialize the date
        dt = datetime.datetime.strptime(strdate, format)
        self = datetime.date.__new__(cls, dt.year, dt.month, dt.day)

        # record format for output
        self._format = format

        # return object
        return self

    def __str__(self):
        return self.strftime(self._format)

    def __add__(self, other):
        return datetime.date.__add__(self, datetime.timedelta(other))

    def __sub__(self, other):
        if isinstance(other, int):
            other = datetime.timedelta(other)
            return datetime.date.__sub__(self, other)

        return datetime.date.__sub__(self, other).days


if __name__ == "__main__":
    d1 = xdate("20170102")
    d2 = xdate("20170202")

    print(d1-d2)
    print(d1+2)
    print(d2-1)