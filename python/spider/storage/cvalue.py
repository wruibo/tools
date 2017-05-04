'''
    value from define table
'''
import re

from utility.ccast import *


class Value:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

    def tosql(self):
        return "not null default %s" % self.tostr()

    def fromsql(self, sql):
        sql = sql.strip()

        regex_value = re.compile(r'(?P<constraint>(not\s+null\s*)?)'
                                 r'(?P<default>(default\s+)?)'
                                 r'(?P<value>([^\s]+)?)',
                                 re.IGNORECASE)
        mobj = regex_value.match(sql)
        if mobj:
            constraint, default, value = mobj.group('constraint', 'default', 'value')
            constraint, default, value = constraint.strip(), default.strip(), value.strip()
            if default:
                ValueCls = [NumberValue, BooleanValue, StringValue]
                for cls in ValueCls:
                    if cls.match(value):
                        return cls(value)
            elif constraint:
                if value == 'auto_increment':
                    return AutoIncValue()
                else:
                    return NotNull()
            else:
                return DefaultNull()

        return DefaultNull()

    def tostr(self):
        return str(self.value)

    def fromstr(self, str):
        ValueCls = [DefaultNull, NotNull, NullValue, AutoIncValue, NumberValue, BooleanValue, StringValue]
        for cls in ValueCls:
            if cls.match(str):
                return cls(str)


class DefaultNull(Value):
    def __init__(self, value="default_null"):
        Value.__init__(self, value)

    def tosql(self):
        return "default null"

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if str == "default_null":
            return True
        return False

class NotNull(Value):
    def __init__(self, value="not_null"):
        Value.__init__(self, value)

    def tosql(self):
        return "not null"

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if str == "not_null":
            return True
        return False

class NullValue(Value):
    def __init__(self, value='null'):
        Value.__init__(self, value)

    def tosql(self):
        return "%s" % self.value

    @staticmethod
    def match(str):
        str = str.strip().lower()
        if str == 'null':
            return True
        return False


class AutoIncValue(Value):
    def __init__(self, value='auto_increment'):
        Value.__init__(self, value)

    def tosql(self):
        return "not null %s" % self.tostr()

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
