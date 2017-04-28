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

    def tostr(self):
        return "%s()" % self.__class__.__name__

    def fromstr(self, str):
        TypeCls = {Int.__name__: Int, BigInt.__name__: BigInt, Float.__name__: Float, Decimal.__name__: Decimal, Boolean.__name__: Boolean, String.__name__: String, Text.__name__: Text}
        type_regex = re.compile(r'^\s*(?P<class>[\w]+)'
                                r'\s*\('
                                r'(?P<args>[\s\w,]*)'
                                r'\)\s*')

        mobj = type_regex.match(str)
        if mobj:
            cls, args = mobj.group('class', 'args')
            if args.strip():
                return TypeCls[cls](*args.split(','))
            else:
                return TypeCls[cls]()

class Int(Type):
    def __init__(self):
        Type.__init__(self)

class BigInt(Type):
    def __init__(self):
        Type.__init__(self)

class Float(Type):
    def __init__(self):
        Type.__init__(self)

class Decimal(Type):
    def __init__(self, length, precision):
        Type.__init__(self)

        self.length = int(length)
        self.precision = int(precision)

    def tostr(self):
        return "%s(%d,%d)" % (self.__class__.__name__, self.length, self.precision)

class Boolean(Type):
    def __init__(self):
        Type.__init__(self)

class String(Type):
    def __init__(self, length):
        Type.__init__(self)

        self.length = int(length)

    def tostr(self):
        return "%s(%d)" % (self.__class__.__name__, self.length)

class Text(Type):
    def __init__(self):
        Type.__init__(self)

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
