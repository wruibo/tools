'''
    type class for field
'''
import re


class Type:
    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        return False

    def tosql(self):
        return self.tostr()

    def fromsql(self, sql):
        TypeCls = {"int": Int, "bigint": BigInt, "float": Float, "decimal": Decimal, "tinyint": Boolean, "varchar": String, "text": Text}
        regex_type = re.compile(r'^\s*(?P<class>[\w]+)'
                                r'\s*\('
                                r'(?P<args>[\s\w,]*)'
                                r'\)\s*')
        mobj = regex_type.match(sql)
        if mobj:
            cls, args = mobj.group('class', 'args')
            cls = cls.lower()
            if args.strip():
                return TypeCls[cls](*args.split(','))
            else:
                return TypeCls[cls]()

    def tostr(self):
        return "%s()" % self.__class__.__name__.lower()

    def fromstr(self, str):
        TypeCls = {Int.__name__.lower(): Int, BigInt.__name__.lower(): BigInt, Float.__name__.lower(): Float, Decimal.__name__.lower(): Decimal, Boolean.__name__.lower(): Boolean, String.__name__.lower(): String, Text.__name__.lower(): Text}
        regex_type = re.compile(r'^\s*(?P<class>[\w]+)'
                                r'\s*\('
                                r'(?P<args>[\s\w,]*)'
                                r'\)\s*')

        mobj = regex_type.match(str)
        if mobj:
            cls, args = mobj.group('class', 'args')
            cls = cls.lower()
            if args.strip():
                return TypeCls[cls](*args.split(','))
            else:
                return TypeCls[cls]()

class Int(Type):
    def __init__(self, *args):
        Type.__init__(self)

    def tosql(self):
        return "int"

class BigInt(Type):
    def __init__(self, *args):
        Type.__init__(self)

    def tosql(self):
        return "bigint"

class Float(Type):
    def __init__(self):
        Type.__init__(self)

    def tosql(self):
        return "float"

class Decimal(Type):
    def __init__(self, length, precision):
        Type.__init__(self)

        self.length = int(length)
        self.precision = int(precision)

    def tosql(self):
        return "decimal(%d,%d)"%(self.length, self.precision)

    def tostr(self):
        return "%s(%d,%d)" % (self.__class__.__name__, self.length, self.precision)

class Boolean(Type):
    def __init__(self, *args):
        Type.__init__(self)

    def tosql(self):
        return "boolean"

class String(Type):
    def __init__(self, length):
        Type.__init__(self)

        self.length = int(length)

    def tosql(self):
        return "varchar(%d)" % self.length

    def tostr(self):
        return "%s(%d)" % (self.__class__.__name__, self.length)

class Text(Type):
    def __init__(self):
        Type.__init__(self)

    def tosql(self):
        return "text"

if __name__ == "__main__":
    type1 = Int()
    type2 = String(12)
    type3 = Decimal(10, 6)

    str1 = type1.tostr()
    str2 = type2.tostr()
    str3 = type3.tostr()

    print str1
    print str2
    print str3

    print Type().fromstr(str1).tostr()
    print Type().fromstr(str2).tostr()
    print Type().fromstr(str3).tostr()
