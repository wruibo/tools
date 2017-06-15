'''
    value from define table
'''
import re

from util.cast import *

NotNullValueError = Exception
AutoIncValueError = Exception


class Value:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

    def default(self):
        return self.value

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
            if value.lower() == 'auto_increment':
                return AutoIncValue()
            elif value.lower() == 'null':
                return DefaultNullValue()
            else:
                vcls = {int.__name__: NumberValue, int.__name__: NumberValue, float.__name__: NumberValue, bool.__name__: BooleanValue, str.__name__: StringValue}
                return vcls[typecls(value).__name__](value)
        else:
            return DefaultNullValue()

    def fromstr(self, str):
        return eval(str)

class DefaultNullValue(Value):
    def __init__(self):
        Value.__init__(self)

    def default(self):
        return 'null'

    def tosql(self):
        return "default null"

    def tostr(self):
        return "%s()" % self.__class__.__name__

class NotNullValue(Value):
    def __init__(self):
        Value.__init__(self)

    def default(self):
        return None

    def tosql(self):
        return "not null"

    def tostr(self):
        return "%s()" % self.__class__.__name__

class AutoIncValue(Value):
    def __init__(self, value='auto_increment'):
        Value.__init__(self, value)
        self.counter = 1

    def default(self):
        return self.counter

    def tosql(self):
        return "not null auto_increment"

    def tostr(self):
        return "%s()" % self.__class__.__name__


class NumberValue(Value):
    def __init__(self, value):
        if isinstance(value, str):
            from util.cast import str2num
            value = str2num(value)

        Value.__init__(self, value)

    def tosql(self):
        return "not null default %s" % num2str(self.value)

    def tostr(self):
        return "%s(%s)" % (self.__class__.__name__, num2str(self.value))

class BooleanValue(Value):
    def __init__(self, value=None):
        if isinstance(value, str):
            value = str2bool(value)
        Value.__init__(self, value)

    def tosql(self):
        return "not null default %s" % bool2str(self.value).lower()

    def tostr(self):
        return "%s(%s)" % (self.__class__.__name__, bool2str(self.value))


class StringValue(Value):
    def __init__(self, value=None):
        value = value.strip("'\"")
        Value.__init__(self, value)

    def tosql(self):
        return "not null default '%s'" % self.value

    def tostr(self):
        return "%s('%s')" % (self.__class__.__name__, self.value)

if __name__ == "__main__":
    value1 = NotNullValue()
    value2 = AutoIncValue()
    value3 = NumberValue(2.1)
    value4 = BooleanValue(True)
    value5 = BooleanValue(False)
    value6 = StringValue('')

    str1 = value1.tostr()
    str2 = value2.tostr()
    str3 = value3.tostr()
    str4 = value4.tostr()
    str5 = value5.tostr()
    str6 = value6.tostr()

    print(str1)
    print(str2)
    print(str3)
    print(str4)
    print(str5)
    print(str6)

    print(Value().fromstr(str1).tostr())
    print(Value().fromstr(str2).tostr())
    print(Value().fromstr(str3).tostr())
    print(Value().fromstr(str4).tostr())
    print(Value().fromstr(str5).tostr())
    print(Value().fromstr(str6).tostr())

    str1 = value1.tosql()
    str2 = value2.tosql()
    str3 = value3.tosql()
    str4 = value4.tosql()
    str5 = value5.tosql()
    str6 = value6.tosql()

    print(str1)
    print(str2)
    print(str3)
    print(str4)
    print(str5)
    print(str6)

    print(Value().fromsql(str1).tosql())
    print(Value().fromsql(str2).tosql())
    print(Value().fromsql(str3).tosql())
    print(Value().fromsql(str4).tosql())
    print(Value().fromsql(str5).tosql())
    print(Value().fromsql(str6).tosql())
