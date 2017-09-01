"""
    type extensions and type relate functions
"""
import datetime, calendar


class Date(datetime.date):
    """
        extends the datetime.date class
    """
    def __new__(cls, year=None, month=None, day=None):
        """
            rewrite datetime.date construct method
        :param year: int/date/str, year of date or date or date string
        :param month: int/str, month of date or date string format
        :param day: int, day of date
        :return:
        """
        # init today's year, month, day
        nyear, nmonth, nday = 1900, 1, 1

        # process input year with str/date/int
        if isinstance(year, str):
            format = month
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear, nmonth, nday = d.year, d.month, d.day
        elif isinstance(year, datetime.date):
            nyear, nmonth, nday = year.year, year.month, year.day
        elif (year is None or isinstance(year, int)) and (month is None or isinstance(month, int)) and (day is None or isinstance(day, int)):
            nyear = year if year is not None else nyear
            nmonth = month if month is not None else nmonth
            nday = day if day is not None else nday
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        return super(Date, cls).__new__(cls, nyear, nmonth, nday)

    def __str__(self):
        return self.strftime('%Y-%m-%d')

    def __add__(self, other):
        """
            add date and time delta
        :param other: obj, date or time delta
        :return:
        """
        if isinstance(other, int) or isinstance(other, float):
            other = DayDelta(int(other))
        elif isinstance(other, YearDelta):
            return Date(self.year+other.years, self.month, self.day)
        elif isinstance(other, QuarterDelta):
            months = self.month + 3*other.quarters if self.month != -3*other.quarters else -12
            year, month = self.year + (months // 13 if months > 0 else months // 12), Month.MONTH_WHEEL[months % 12]
            return Date(year, month, self.day)
        elif isinstance(other, MonthDelta):
            months = self.month + other.months if self.month != -other.months else -12
            year, month = self.year + (months // 13 if months > 0 else months // 12), Month.MONTH_WHEEL[months % 12]
            return Date(year, month, self.day)

        return Date(datetime.date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = DayDelta(int(other))
        elif isinstance(other, YearDelta):
            return Date(self.year-other.years, self.month, self.day)
        elif isinstance(other, QuarterDelta):
            months = self.month - 3*other.quarters if self.month != 3*other.quarters else -12
            year, month = self.year + (months // 13 if months > 0 else months // 12), Month.MONTH_WHEEL[months % 12]
            return Date(year, month, self.day)
        elif isinstance(other, MonthDelta):
            months = self.month - other.months if self.month != other.months else -12
            year, month = self.year + (months // 13 if months > 0 else months // 12), Month.MONTH_WHEEL[months % 12]
            return Date(year, month, self.day)

        result = datetime.date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        return result

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def days(self):
        return 1

    @classmethod
    def today(cls):
      return Date(super(Date, cls).today())

    @staticmethod
    def delta(days):
        return DayDelta(days)

    @staticmethod
    def unit_days():
        return 1

    @staticmethod
    def working_days():
        return 1

    @staticmethod
    def trading_days():
        return 1

    @staticmethod
    def yearly_units():
        return 365

    @staticmethod
    def yearly_trading_units():
        return 252


class Time(datetime.time):
    """
        time
    """
    def __new__(cls, time=None, format=None):
        if isinstance(time, str):
            if format is None or not isinstance(format, str):
                raise ValueError("format must be specified.")
            time = datetime.datetime.strptime(time, format)

        if time is None:
            time = datetime.datetime.now()

        return super(Time, cls).__new__(cls, time.hour, time.minute, time.second, time.microsecond)


class DateTime(datetime.datetime):
    """
        date time
    """
    def __new__(cls, dt, format=None):
        if isinstance(dt, str):
            if format is None or not isinstance(format, str):
                raise ValueError("format must be specified.")
                dt = datetime.datetime.strptime(dt, format)
        elif dt is None:
            dt = datetime.datetime.now()
        elif isinstance(dt, datetime.datetime):
            pass
        elif isinstance(dt, datetime.date):
            dt = datetime.datetime(dt.year, dt.month, dt.day)

        return super(DateTime, cls).__new__(cls, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)


class DateRange(object):
    """
        range day class
    """
    def __init__(self, start_date, end_date, format="%Y-%m-%d"):
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
        assert isinstance(other, DateRange)
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


class Year(Date):
    def __new__(cls, year=None, format=None):
        """
            rewrite datetime.date construct method
        :param year: int/date/str, year of date or date or date string
        :param month: int/str, month of date or date string format
        :param day: int, day of date
        :return:
        """
        # init today's year, month, day
        nyear = 1900

        # process input year with str/date/int
        if isinstance(year, str):
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear = d.year
        elif isinstance(year, datetime.date):
            nyear = year.year
        elif (year is None or isinstance(year, int)):
            nyear = year if year is not None else nyear
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        return super(Year, cls).__new__(cls, nyear, 1, 1)

    def __str__(self):
        return "%s" % str(self.year).rjust(4, '0')

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            year = self.year+int(other)
            return Year(year)

        return Year(Date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            year = self.year-int(other)
            return Year(year)

        result = Date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        elif isinstance(result, int):
            return result
        else:
            return Year(result)

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def days(self):
        return 365

    @staticmethod
    def delta(years):
        return YearDelta(years)

    @staticmethod
    def unit_days():
        return 365

    @staticmethod
    def working_days():
        return 252

    @staticmethod
    def trading_days():
        return 252

    @staticmethod
    def yearly_units():
        return 1

    @staticmethod
    def yearly_trading_units():
        return 1


class Quarter(Date):
    # month correspond quarter number of year
    MONTH_QUARTER = {
        1:1, 2:1, 3:1,
        4:2, 5:2, 6:2,
        7:3, 8:3, 9:3,
        10:4, 11:4, 12:4
    }

    # quarter correspond months
    QUARTER_MONTH = {
        1:[1, 2, 3],
        2:[4, 5, 6],
        3:[7, 8, 9],
        4:[10, 11, 12]
    }


    def __new__(cls, year=None, month=None):
        """
            rewrite datetime.date construct method
        :param year: int/date/str, year of date or date or date string
        :param month: int/str, month of date or date string format
        :return:
        """
        # init today's year, month, day
        nyear, nmonth = 1900, 1

        # process input year with str/date/int
        if isinstance(year, str):
            format = month
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear, nmonth = d.year, d.month
        elif isinstance(year, datetime.date):
            nyear, nmonth, nday = year.year, year.month, year.day
        elif (year is None or isinstance(year, int)) and (month is None or isinstance(month, int)):
            nyear = year if year is not None else nyear
            nmonth = month if month is not None else nmonth
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        quarter = Quarter.MONTH_QUARTER[nmonth]
        nmonth = Quarter.QUARTER_MONTH[quarter][0]

        self = super(Quarter, cls).__new__(cls, nyear, nmonth, 1)
        self._quarter = quarter

        return self

    def __str__(self):
        return "%sQ%s" % (str(self.year).rjust(4, '0'), str(self.quarter).rjust(2, '0'))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = 3*(int(other))
            months = self.month+other if self.month!=-other else -12
            year, month = self.year + (months//13 if months>0 else months//12),  Month.MONTH_WHEEL[months%12]
            return Quarter(year, month)

        return Quarter(Date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = 3 * (int(other))
            months = self.month-other if self.month!=other else -12
            year, month = self.year + (months//13 if months>0 else months//12),  Month.MONTH_WHEEL[months%12]
            return Quarter(year, month)

        result = Date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        elif isinstance(result, int):
            return result
        else:
            return Quarter(result)

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def quarter(self):
        return self._quarter

    @property
    def days(self):
        return sum([calendar.monthrange(self.year, m)[1] for m in Quarter.QUARTER_MONTH[self.quarter]])

    @staticmethod
    def delta(quarters):
        return QuarterDelta(quarters)

    @staticmethod
    def unit_days():
        return 90

    @staticmethod
    def working_days():
        return 66

    @staticmethod
    def trading_days():
        return 66

    @staticmethod
    def yearly_units():
        return 4

    @staticmethod
    def yearly_trading_units():
        return 4


class Month(Date):
    MONTH_WHEEL = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def __new__(cls, year=None, month=None):
        """
            rewrite datetime.date construct method
        :param year: int/date/str, year of date or date or date string
        :param month: int/str, month of date or date string format
        :param day: int, day of date
        :return:
        """
        # init today's year, month, day
        nyear, nmonth = 1900, 1

        # process input year with str/date/int
        if isinstance(year, str):
            format = month
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear, nmonth, nday = d.year, d.month, d.day
        elif isinstance(year, datetime.date):
            nyear, nmonth, nday = year.year, year.month, year.day
        elif (year is None or isinstance(year, int)) and (month is None or isinstance(month, int)):
            nyear = year if year is not None else nyear
            nmonth = month if month is not None else nmonth
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        return super(Month, cls).__new__(cls, nyear, nmonth, 1)

    def __str__(self):
        return "%sM%s" % (str(self.year).rjust(4, '0'), str(self.month).rjust(2, '0'))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            months = self.month+int(other) if self.month!=-int(other) else -12
            year, month = self.year + (months//13 if months>0 else months//12),  Month.MONTH_WHEEL[months%12]
            return Month(year, month)

        return Month(Date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            months = self.month-int(other) if self.month!=int(other) else -12
            year, month = self.year + (months//13 if months>0 else months//12),  Month.MONTH_WHEEL[months%12]
            return Month(year, month)

        result = Date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        elif isinstance(result, int):
            return result
        else:
            return Month(result)

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def days(self):
        return calendar.monthrange(self.year, self.month)[1]

    @staticmethod
    def delta(months):
        return MonthDelta(months)

    @staticmethod
    def unit_days():
        return 30

    @staticmethod
    def working_days():
        return 22

    @staticmethod
    def trading_days():
        return 22

    @staticmethod
    def yearly_units():
        return 12

    @staticmethod
    def yearly_trading_units():
        return 12


class Week(Date):
    def __new__(cls, year=None, month=None, day=None):
        # init today's year, month, day
        nyear, nmonth, nday = 1900, 1, 1

        # process input year with str/date/int
        if isinstance(year, str):
            format = month
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear, nmonth, nday = d.year, d.month, d.day
        elif isinstance(year, datetime.date):
            nyear, nmonth, nday = year.year, year.month, year.day
        elif (year is None or isinstance(year, int)) and (month is None or isinstance(month, int)) and (day is None or isinstance(day, int)):
            nyear = year if year is not None else nyear
            nmonth = month if month is not None else nmonth
            nday = day if day is not None else nday
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        dt = datetime.date(nyear, nmonth, nday)
        mdt = dt - datetime.timedelta(dt.weekday())
        nyear, nmonth, nday = mdt.year, mdt.month, mdt.day

        self = super(Week, cls).__new__(cls, nyear, nmonth, nday)
        self._week = self.isocalendar()[1]

        return self

    def __str__(self):
        return "%sW%s" % (str(self.year).rjust(4, '0'), str(self.week).rjust(2, '0'))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = TimeDelta(weeks=int(other))
        return Week(Date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = TimeDelta(weeks=int(other))

        result = Date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        elif isinstance(result, int):
            return result
        else:
            return Week(result)

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def week(self):
        return self._week

    @property
    def days(self):
        return 7

    @staticmethod
    def delta(weeks):
        return WeekDelta(weeks)

    @staticmethod
    def unit_days():
        return 7

    @staticmethod
    def working_days():
        return 5

    @staticmethod
    def trading_days():
        return 5

    @staticmethod
    def yearly_units():
        return 52

    @staticmethod
    def yearly_trading_units():
        return 52


class Day(Date):
    """
        extends the datetime.date class
    """
    def __new__(cls, year=None, month=None, day=None):
        """
            rewrite datetime.date construct method
        :param year: int/date/str, year of date or date or date string
        :param month: int/str, month of date or date string format
        :param day: int, day of date
        :return:
        """
        # init today's year, month, day
        nyear, nmonth, nday = 1900, 1, 1

        # process input year with str/date/int
        if isinstance(year, str):
            format = month
            if format is None or not isinstance(format, str):
                raise ValueError("date string format must be specified.")
            d = datetime.datetime.strptime(year, format)
            nyear, nmonth, nday = d.year, d.month, d.day
        elif isinstance(year, datetime.date):
            nyear, nmonth, nday = year.year, year.month, year.day
        elif (year is None or isinstance(year, int)) and (month is None or isinstance(month, int)) and (day is None or isinstance(day, int)):
            nyear = year if year is not None else nyear
            nmonth = month if month is not None else nmonth
            nday = day if day is not None else nday
        else:
            raise ValueError("(date string, date string format) / (date object) / (year<int/None>, month<int/None>, day<int/None>) wanted")

        return super(Day, cls).__new__(cls, nyear, nmonth, nday)

    def __str__(self):
        return self.strftime('%Y-%m-%d')

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = TimeDelta(days=int(other))
        return Day(Date.__add__(self, other))

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = TimeDelta(days=int(other))

        result = Date.__sub__(self, other)
        if isinstance(result, datetime.timedelta):
            return result.days
        elif isinstance(result, int):
            return result
        else:
            return Day(result)

    __radd__ = __add__
    __rsub__ = __sub__

    @property
    def days(self):
        return 1

    @staticmethod
    def delta(days):
        return DayDelta(days)

    @staticmethod
    def unit_days():
        return 1

    @staticmethod
    def working_days():
        return 1

    @staticmethod
    def trading_days():
        return 1

    @staticmethod
    def yearly_units():
        return 365

    @staticmethod
    def yearly_trading_units():
        return 252

class TimeDelta(datetime.timedelta):
    """
        time delta
    """

    def __new__(cls, years=0, quarters=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        self = super(TimeDelta, cls).__new__(cls, days, seconds, microseconds, milliseconds, minutes, hours, weeks)
        self._years, self._quarters, self._months = years, quarters, months
        return self

    @property
    def years(self):
        return self._years

    @property
    def quarters(self):
        return self._quarters

    @property
    def months(self):
        return self._months


class DayDelta(TimeDelta):
    def __new__(cls, days):
        return super(DayDelta, cls).__new__(cls, days=days)


class WeekDelta(TimeDelta):
    def __new__(cls, weeks):
        return super(WeekDelta, cls).__new__(cls, weeks=weeks)


class MonthDelta(TimeDelta):
    def __new__(cls, months):
        return super(MonthDelta, cls).__new__(cls, months=months)


class QuarterDelta(TimeDelta):
    def __new__(cls, quarters):
        return super(QuarterDelta, cls).__new__(cls, quarters=quarters)


class YearDelta(TimeDelta):
    def __new__(cls, years):
        return super(YearDelta, cls).__new__(cls, years=years)


date = Date
day = Day
year = Year
quarter = Quarter
month = Month
week = Week
daterange = DateRange


if __name__ == "__main__":
    m = Month(2016, 8)
    y = Year(2016)

    print(y-m)
    print(m-y)