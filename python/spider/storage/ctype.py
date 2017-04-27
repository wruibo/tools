class Type:
    def __init__(self):
        pass

    class Base:
        def __init__(self):
            pass

        def tostr(self):
            return "%s()" % self.__class__.__name__

    class Int(Base):
        def __init__(self):
            Type.Base.__init__(self)

    class BigInt(Base):
        def __init__(self):
            Type.Base.__init__(self)

    class Float(Base):
        def __init__(self):
            Type.Base.__init__(self)

    class Decimal(Base):
        def __init__(self, length, precision):
            Type.Base.__init__(self)

            self.length = int(length)
            self.precision = int(precision)

        def tostr(self):
            return "%s(%d,%d)" % (self.__class__.__name__, self.length, self.precision)

    class Boolean(Base):
        def __init__(self):
            Type.Base.__init__(self)

    class String(Base):
        def __init__(self, length):
            Type.Base.__init__(self)

            self.length = int(length)

        def tostr(self):
            return "%s(%d)" % (self.__class__.__name__, self.length)

    class Text(Base):
        def __init__(self):
            Type.Base.__init__(self)

    TypeCls = {Int.__name__: Int, BigInt.__name__: BigInt, Float.__name__: Float, Decimal.__name__: Decimal, Boolean.__name__:Boolean, String.__name__:String, Text.__name__:Text}
    @staticmethod
    def fromstr(str):
        import re
        type_regex = re.compile(r'^\s*(?P<class>[\w]+)'
                                r'\s*\('
                                r'(?P<args>[\s\w,]*)'
                                r'\)\s*')

        mobj = type_regex.match(str)
        if mobj:
            cls, args = mobj.group('class', 'args')
            if args.strip():
                return Type.TypeCls[cls](*args.split(','))
            else:
                return Type.TypeCls[cls]()


if __name__ == "__main__":
    type1 = Type.Int()
    type2 = Type.String(12)
    type3 = Type.Decimal(10, 6)

    str1 = type1.tostr()
    str2 = type2.tostr()
    str3 = type3.tostr()

    print str1
    print str2
    print str3

    print Type.fromstr(str1).tostr()
    print Type.fromstr(str2).tostr()
    print Type.fromstr(str3).tostr()
