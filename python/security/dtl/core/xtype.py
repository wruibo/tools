"""
    type extensions and type relate functions
"""
import math, datetime, calendar

__all__ = ["xdate", "xweek", "xmonth", "xquarter", "xyear", "xrangeday"]

# default date string format
_default_date_format = "%Y-%m-%d"


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

    @property
    def days(self):
        return 1

    @staticmethod
    def unitdays():
        return 7

    def date(self):
        return self

    def back(self, periodcls, periods):
        if periodcls==xdate or periodcls==xday:
            return xdate(self-datetime.timedelta(periods))
        elif periodcls==xweek:
            return xdate(self - datetime.timedelta(weeks=periods))
        elif periodcls==xmonth:
            month = xmonth(self)-periods
            return xdate(datetime.date(month.year, month.month, self.day))
        elif periodcls==xquarter:
            month = xmonth(self) - 3*periods
            return xdate(datetime.date(month.year, month.month, self.day))
        elif periodcls==xyear:
            return xdate(datetime.date(self.year-periods, self.month, self.day))
        else:
            raise "unsupport period class: %s" % periodcls.__name__

    def forward(self, periodcls, periods):
        if periodcls==xdate or periodcls==xday:
            return xdate(self+datetime.timedelta(periods))
        elif periodcls==xweek:
            return xdate(self + datetime.timedelta(weeks=periods))
        elif periodcls==xmonth:
            month = xmonth(self)+periods
            return xdate(datetime.date(month.year, month.month, self.day))
        elif periodcls==xquarter:
            month = xmonth(self) + 3*periods
            return xdate(datetime.date(month.year, month.month, self.day))
        elif periodcls==xyear:
            return xdate(datetime.date(self.year+periods, self.month, self.day))
        else:
            raise "unsupport period class: %s" % periodcls.__name__

    def __str__(self):
        return self.strftime(self._format)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = datetime.timedelta(int(other))
        return xdate(datetime.date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = datetime.timedelta(int(other))

        result = datetime.date.__sub__(self, other)

        if isinstance(result, datetime.timedelta):
            return result.days
        return result


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


class xperiod(object):
    """
        time period base class
    """
    pass


class xday(xperiod):
    """
        day class of period
    """
    def __init__(self, date = datetime.date.today(), format=_default_date_format):
        # format string date to datetime object if input date is string object
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, format)

        if hasattr(date, 'date'):
            date = date.date()

        # initialize the date
        self._date = date

        # record format for output
        self._format = format if format is not None else _default_date_format

    @property
    def year(self):
        return self._date.year

    @property
    def quarter(self):
        return xquarter.detect(self._date)

    @property
    def month(self):
        return self._date.month

    @property
    def week(self):
        return self._date.isoweekday()

    @property
    def day(self):
        return self._date.day

    @property
    def days(self):
        return 1

    @staticmethod
    def unitdays():
        return 1

    def date(self):
        return self._date

    def back(self, periodcls, periods):
        if periodcls==xdate or periodcls==xday:
            return xday(self-datetime.timedelta(periods))
        elif periodcls==xweek:
            return xday(self - datetime.timedelta(weeks=periods))
        elif periodcls==xmonth:
            month = xmonth(self)-periods
            return xday(datetime.date(month.year, month.month, self.day))
        elif periodcls==xquarter:
            month = xday(self) - 3*periods
            return xdate(datetime.date(month.year, month.month, self.day))
        elif periodcls==xyear:
            return xday(datetime.date(self.year-periods, self.month, self.day))
        else:
            raise "unsupport period class: %s" % periodcls.__name__

    def forward(self, periodcls, periods):
        if periodcls==xdate or periodcls==xday:
            return xday(self+datetime.timedelta(periods))
        elif periodcls==xweek:
            return xday(self + datetime.timedelta(weeks=periods))
        elif periodcls==xmonth:
            month = xmonth(self)+periods
            return xday(datetime.date(month.year, month.month, self.day))
        elif periodcls==xquarter:
            month = xmonth(self) + 3*periods
            return xday(datetime.date(month.year, month.month, self.day))
        elif periodcls==xyear:
            return xday(datetime.date(self.year+periods, self.month, self.day))
        else:
            raise "unsupport period class: %s" % periodcls.__name__

    def __str__(self):
        return self._date.strftime(self._format)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.year<<16 + self.month<<8 + self.day

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = datetime.timedelta(int(other))
        else:
            raise "xday can not add with: %s" % other.__class__.__name__

        return xday(self._date + other, self._format)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = datetime.timedelta(int(other))

        if hasattr(other, "date"):
            other = other.date()

        if not (isinstance(other, datetime.date) or isinstance(other, datetime.timedelta)):
            raise "xday can not sub with: %s" % other.__class__.__name__

        result = self._date - other

        if isinstance(result, datetime.timedelta):
            return result.days

        return xday(result, self._format)

    __radd__ = __add__
    __rsub__ = __sub__

    def __cmp__(self, other):
        if isinstance(other, xdate) or isinstance(other, xday) or isinstance(other, datetime.date) or isinstance(other, datetime.datetime):
            return 0 if (self.year, self.month, self.day) == (other.year, other.month, other.day) else 1 if (self.year, self.month, self.day) > (other.year, other.month, other.day) else -1
        elif isinstance(other, xweek):
            return 0 if (self.year, self.week) == (other.year, other.week) else 1 if (self.year, self.week) > (other.year, other.week) else -1
        elif isinstance(other, xmonth):
            return 0 if (self.year, self.month) == (other.year, other.month) else 1 if (self.year, self.month) > (other.year, other.month) else -1
        elif isinstance(other, xquarter):
            return 0 if (self.year, self.quarter) == (other.year, other.quarter) else 1 if (self.year, self.quarter) > (other.year, other.quarter) else -1
        elif isinstance(other, xyear):
            return 0 if self.year == other.year else 1 if self.year > other.year else -1
        else:
            raise "xday can not compare with: %s" % other.__class__.__name__

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


class xweek(xperiod):
    """
        week class of period
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

    @staticmethod
    def unitdays():
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


class xmonth(xperiod):
    """
        month class of period
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

    @staticmethod
    def unitdays():
        return 30

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


class xquarter(xperiod):
    """
            quarter class of period
    """
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

    @staticmethod
    def unitdays():
        return 90

    @staticmethod
    def detect(obj):
        if not hasattr(obj, 'month'):
            raise "xquarter can not detect for: %s" % obj.__class__.__name__

        return xquarter._month_quarter[obj.month]


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


class xyear(xperiod):
    """
        year class of period
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

    @staticmethod
    def unitdays():
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
    week1 = xweek("2015-01-01")
    print("+++++++")
    for i in range(0, 120):
        week1 += 3
        print(week1)
    print("--------")
    for i in range(0, 120):
        print(week1)
        week1 -= 3

    print("+++++++")
    month1 = xmonth("2015-01-01")
    for i in range(0, 30):
        month1 += 11
        print(month1)
    print("--------")
    for i in range(0, 30):
        print(month1)
        month1 -= 11

    print("+++++++")
    quarter1 = xquarter("2015-01-01")
    for i in range(0, 30):
        quarter1 += 4
        print(quarter1)
    print("--------")
    for i in range(0, 30):
        print(quarter1)
        quarter1 -= 4

    print("+++++++")
    day1 = xday()
    for i in range(0, 33):
        day1 += 1
        print(day1)
    print("--------")
    for i in range(0, 33):
        day1 -= 1
        print(day1)

    print(xquarter("2015-08-01").days)

    print(xrangeday("2015-02-01", "2015-03-01").days)

    print(xdate().back(xweek, 2))
    print(xdate().forward(xweek, 2))

