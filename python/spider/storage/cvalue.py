'''
    value from define table
'''
from utility.ccast import *

class Value:
    def __init__(self):
        pass

    class Base:
        def __init__(self, value):
            self._value = value

        @property
        def value(self):
            return self._value

        def tostr(self):
            return str(self._value)

    class Null(Base):
        def __init__(self, value='null'):
            Value.Base.__init__(self, value)

        @staticmethod
        def match(str):
            str = str.strip().lower()
            if str == 'null':
                return True
            return False

    class AutoInc(Base):
        def __init__(self, value='auto_increment'):
            Value.Base.__init__(self, value)

        @staticmethod
        def match(str):
            str = str.strip().lower()
            if str == 'auto_increment':
                return True
            return False

    class Number(Base):
        def __init__(self, value=None):
            if isinstance(value, str):
                from utility.ccast import str2num
                value = str2num(value)

            Value.Base.__init__(self, value)

        @staticmethod
        def match(str):
            from utility.ccast import isnum
            return isnum(str)

    class Boolean(Base):
        def __init__(self, value=None):
            if isinstance(value, str):
                value = str2bool(value)
            Value.Base.__init__(self, value)

        @staticmethod
        def match(str):
            return isbool(str)

    class String(Base):
        def __init__(self, value=None):
            value = value.strip("'\"")
            Value.Base.__init__(self, value)

        def tostr(self):
            return "'%s'" % self.value

        @staticmethod
        def match(str):
            str = str.strip().lower()
            if (str[0] == "'" or str[0] == '"') and (str[-1] == "'" or str[-1] == '"'):
                return True
            return False

    @staticmethod
    def fromstr(str):
        ValueCls = [Value.Null, Value.AutoInc, Value.Number, Value.Boolean, Value.String]
        for cls in ValueCls:
            if cls.match(str):
                return cls(str)
        return None

if __name__ == "__main__":
    value1 = Value.Null()
    value2 = Value.AutoInc()
    value3 = Value.Number(2.1)
    value4 = Value.Boolean(True)
    value5 = Value.Boolean(False)
    value6 = Value.String('abcde')

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

    print Value.fromstr(str1).tostr()
    print Value.fromstr(str2).tostr()
    print Value.fromstr(str3).tostr()
    print Value.fromstr(str4).tostr()
    print Value.fromstr(str5).tostr()
    print Value.fromstr(str6).tostr()
