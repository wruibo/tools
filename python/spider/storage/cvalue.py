'''
    value from define table
'''
from utility.ccast import *


class Value:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

    def tostr(self):
        return str(self.value)

    def fromstr(self, str):
        ValueCls = [NullValue, AutoIncValue, NumberValue, BooleanValue, StringValue]
        for cls in ValueCls:
            if cls.match(str):
                return cls(str)


class NullValue(Value):
    def __init__(self, value='null'):
        Value.__init__(self, value)

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if str == 'null':
            return True
        return False


class AutoIncValue(Value):
    def __init__(self, value='auto_increment'):
        Value.__init__(self, value)

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if str == 'auto_increment':
            return True
        return False


class NumberValue(Value):
    def __init__(self, value=None):
        if isinstance(value, str):
            from utility.ccast import str2num
            value = str2num(value)

        Value.__init__(self, value)

    @staticmethod
    def match(str):
        from utility.ccast import isnum
        return isnum(str)


class BooleanValue(Value):
    def __init__(self, value=None):
        if isinstance(value, str):
            value = str2bool(value)
        Value.__init__(self, value)

    @staticmethod
    def match(str):
        return isbool(str)


class StringValue(Value):
    def __init__(self, value=None):
        value = value.strip("'\"")
        Value.__init__(self, value)

    def tostr(self):
        return "'%s'" % self.value

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if (str[0] == "'" or str[0] == '"') and (str[-1] == "'" or str[-1] == '"'):
            return True
        return False

if __name__ == "__main__":
    value1 = NullValue()
    value2 = AutoIncValue()
    value3 = NumberValue(2.1)
    value4 = BooleanValue(True)
    value5 = BooleanValue(False)
    value6 = StringValue('abcde')

    str1 = value1.tostr()
    str2 = value2.tostr()
    str3 = value3.tostr()
    str4 = value4.tostr()
    str5 = value5.tostr()
    str6 = value6.tostr()

    print str1
    print str2
    print str3
    print str4
    print str5
    print str6

    print Value().fromstr(str1).tostr()
    print Value().fromstr(str2).tostr()
    print Value().fromstr(str3).tostr()
    print Value().fromstr(str4).tostr()
    print Value().fromstr(str5).tostr()
    print Value().fromstr(str6).tostr()
