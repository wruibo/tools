"""
    type extensions and type relate functions
"""
import datetime, calendar

__all__ = ["xdate", "xweek", "xmonth", "xquarter", "xyear"]

# default date string format
_default_date_format = "%Y%m%d"


class xdate(datetime.date):
    """
        extends the datetime.date class
    """
    def __new__(cls, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        # initialize the date
        self = datetime.date.__new__(cls, date.year, date.month, date.day)

        # record format for output
        self._format = format if format is not None else _default_date_format

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



class xweek(object):
    """
        week class for data
    """
    def __init__(self, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        # save the year, week number of year, week day of sepcified date
        self._year, self._week, weekday = date.isocalendar()

        # save monday date of the week
        self._monday = date - datetime.timedelta(weekday-1)

    @property
    def year(self):
        return self._year

    @property
    def week(self):
        return self._week

    def __str__(self):
        return "%sW%s" % (str(self._year).zfill(4), str(self._week).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        assert isinstance(other, int)
        # new monday date
        self._monday = self._monday+datetime.timedelta(7*other)

        # new year, week number
        self._year, self._week = self._monday.isocalendar()[0:2]

        return self

    def __sub__(self, other):
        assert isinstance(other, int)

        # new monday date
        self._monday = self._monday-datetime.timedelta(7*other)

        # new year, week number
        self._year, self._week = self._monday.isocalendar()[0:2]

        return self

    __radd__ = __add__
    __rsub__ = __sub__

    def __cmp__(self, other):
        assert isinstance(other, xweek) or isinstance(other, xdate) or isinstance(other, datetime.date) or isinstance(other, datetime.datetime)
        year, week = None, None

        if isinstance(other, xweek):
            year, week = other.year, other.week
        else:
            year, week = other.isocalendar()[0:2]

        return 0 if (self.year, self.week)==(year, week) else 1 if (self.year, self.week)>(year, week) else -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0


class xmonth():
    """
        month class for data
    """
    def __init__(self, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        # save the year, month of year
        self._year, self._month = date.year, date.month

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    def __str__(self):
        return "%sM%s" % (str(self._year).zfill(4), str(self._month).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._month, self._year = (self._month+other) % 13, self._year+int((self._month+other)/12)
        if self._month==0: self._month, self._year = (1, self._year-1)

        return self


    def __sub__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._month, self._year = (self._month-other) % 12, self._year + int((self._month-other)/12)
        if self._month==0: self._month, self._year = (12, self._year-1)

        return self

    __radd__ = __add__
    __rsub__ = __sub__

    def __cmp__(self, other):
        assert isinstance(other, xmonth) or isinstance(other, xdate) or isinstance(other, datetime.date) or isinstance(other, datetime.datetime)
        year, month = other.year, other.month

        return 0 if (self.year, self.month)==(year, month) else 1 if (self.year, self.month)>(year, month) else -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0


class xquarter():
    # month correspond quarter number of year
    _month_quarter = {
        1:1, 2:1, 3:1,
        4:2, 5:2, 6:2,
        7:3, 8:3, 9:3,
        10:4, 11:4, 12:4
    }

    """
        quarter class for data
    """
    def __init__(self, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        # save the year, quarter of year
        self._year, self._quarter = date.year, xquarter._month_quarter[date.month]

    @property
    def year(self):
        return self._year

    @property
    def quarter(self):
        return self._quarter


    def __str__(self):
        return "%sQ%s" % (str(self._year).zfill(4), str(self._quarter).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._quarter = (self._quarter+other) % 4
        self._year += int((self._quarter+other)/4)

        return self


    def __sub__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._quarter = (self._quarter-other) % 4
        self._year += int((self.quarter-other)/4)

        return self

    __radd__ = __add__
    __rsub__ = __sub__

    def __cmp__(self, other):
        assert isinstance(other, xquarter) or isinstance(other, xdate) or isinstance(other, datetime.date) or isinstance(other, datetime.datetime)

        year, quarter = (other.year, other.quarter) if isinstance(other, xquarter) else (other.year, xquarter._month_quarter[other.month])

        return 0 if (self.year, self.quarter)==(year, quarter) else 1 if (self.year, self.quarter)>(year, quarter) else -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0


class xyear():
    """
        year class for data
    """
    def __init__(self, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        # save the year
        self._year  = date.year

    @property
    def year(self):
        return self._year

    def __str__(self):
        return "%s" % str(self._year).zfill(4)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        assert isinstance(other, int)

        # new year
        self._year += other

        return self

    def __sub__(self, other):
        assert isinstance(other, int)

        # new year
        self._year -= other

        return self

    __radd__ = __add__
    __rsub__ = __sub__

    def __cmp__(self, other):
        assert isinstance(other, xyear) or isinstance(other, xdate) or isinstance(other, datetime.date) or isinstance(other, datetime.datetime)

        return 0 if self.year==other.year else 1 if self.year > other.year else -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0


if __name__ == "__main__":
    print(xweek("20151231")==xdate("20151227"))
    print(xweek("20151231")+56)
    print(xweek("20151231") - 54)

    print(xmonth("20151231"))
    print(xmonth("20151231") + 12)
    print(xmonth("20151231") - 12)