"""
    type extensions and type relate functions
"""
import math, datetime, calendar

__all__ = ["xdate", "xweek", "xmonth", "xquarter", "xyear", "xrangeday"]

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

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return datetime.date.__add__(self, datetime.timedelta(other))

    def __sub__(self, other):
        if isinstance(other, int):
            other = datetime.timedelta(other)
            return datetime.date.__sub__(self, other)

        return datetime.date.__sub__(self, other).days


class xrangeday(object):
    """
        range day class
    """
    def __init__(self, start_date, end_date, format=_default_date_format):
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, format).date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, format).date()

        self._start_date = start_date.date() if hasattr(start_date, 'date') else start_date
        self._end_date = end_date.date() if hasattr(end_date, 'date') else end_date

        self._format = format

    @property
    def startd(self):
        return self._start_date

    @property
    def endd(self):
        return self._end_date

    @property
    def days(self):
        return (self._end_date-self._start_date).days

    def __str__(self):
        return "%s~%s" % (self._start_date.strftime(self._format), self._end_date.strftime(self._format))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.startd.year<<16+self.startd.month<<8+self.startd.day

    def __cmp__(self, other):
        assert isinstance(other, xrangeday)
        return 0 if self._start_date == other.startd else 1 if self._start_date>other.startd else -1

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

    @property
    def days(self):
        return 7

    def __str__(self):
        return "%sW%s" % (str(self._year).zfill(4), str(self._week).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.year<<8 + self._week

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

    @property
    def days(self):
        return calendar.monthrange(self.year, self.month)[1]

    def __str__(self):
        return "%sM%s" % (str(self._year).zfill(4), str(self._month).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.year<<8+self.month

    def __add__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._month, self._year = (self._month+other) % 12, self._year+int((self._month+other)/12)
        if self._month==0: self._month, self._year = (12, self._year-1)

        return self


    def __sub__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._month, self._year = (self._month-other) % 12, self._year + math.floor((self._month-other)/12)
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

    # quarter correspond months
    _quarter_month = {
        1:[1, 2, 3],
        2:[4, 5, 6],
        3:[7, 8, 9],
        4:[10, 11, 12]
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

    @property
    def days(self):
        return sum([calendar.monthrange(self.year, m)[1] for m in xquarter._quarter_month[self._quarter]])


    def __str__(self):
        return "%sQ%s" % (str(self._year).zfill(4), str(self._quarter).zfill(2))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.year<<8+self.quarter

    def __add__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._quarter, self._year = (self._quarter+other) % 4, self._year+int((self._quarter+other)/4)
        if self._quarter == 0: self._quarter, self._year = (4, self._year-1)

        return self

    def __sub__(self, other):
        assert isinstance(other, int)

        # new year and month
        self._quarter, self._year = (self._quarter-other) % 4, self._year+math.floor((self._quarter-other)/4)
        if self._quarter == 0: self._quarter, self._year = (4, self._year-1)

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

    @property
    def days(self):
        return 365

    def __str__(self):
        return "%s" % str(self._year).zfill(4)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.year

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
    week1 = xweek("20150101")
    print("+++++++")
    for i in range(0, 120):
        week1 += 3
        print(week1)
    print("--------")
    for i in range(0, 120):
        print(week1)
        week1 -= 3

    print("+++++++")
    month1 = xmonth("20150101")
    for i in range(0, 30):
        month1 += 11
        print(month1)
    print("--------")
    for i in range(0, 30):
        print(month1)
        month1 -= 11

    print("+++++++")
    quarter1 = xquarter("20150101")
    for i in range(0, 30):
        quarter1 += 4
        print(quarter1)
    print("--------")
    for i in range(0, 30):
        print(quarter1)
        quarter1 -= 4

    print(xquarter("20150801").days)

    print(xrangeday("20150201", "20150301").days())