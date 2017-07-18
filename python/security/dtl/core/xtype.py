"""
    type extensions and type relate functions
"""
import datetime

__all__ = ["xday"]

class xday(object):
    def __init__(self, date, format):
        self._format = format
        if isinstance(date, str):
            self._date = datetime.datetime.strptime(date, format)
        else:
            self._date = date

    @property
    def date(self):
        return self._date

    def __str__(self):
        return self._date.strftime(self._format)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise "xday can't compare with %s" % other.__class___
        return self._date > other.date

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise "xday can't compare with %s" % other.__class___
        return self._date < other.date

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise "xday can't compare with %s" % other.__class___
        return self._date == other.date

    def __add__(self, days):
        return xday(self._date + datetime.timedelta(days), self._format)

    def __sub__(self, day):
        if isinstance(day, int):
            return self._date - datetime.timedelta(day)

        return abs((self._date - day.date).days)