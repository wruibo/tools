
class Type:
    def __init__(self):
        pass

    class Base:
        def __init__(self):
            pass

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

            self.length = length
            self.precision = precision

    class Boolean(Base):
        def __init__(self):
            Type.Base.__init__(self)

    class String(Base):
        def __init__(self, length):
            Type.Base.__init__(self)

            self.length = length

    class Text(Base):
        def __init__(self):
            Type.Base.__init__(self)


class Value:
    def __init__(self):
        pass

    class Base:
        def __init__(self, value):
            self.value = value

    class Null(Base):
        def __init__(self):
            Value.Base.__init__(self, None)

    class AutoInc(Base):
        def __init__(self):
            Value.Base.__init__(self, None)

    class Int(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class BigInt(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class Float(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class Decimal(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class Boolean(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class String(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

    class Text(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)


class Field:
    def __init__(self, name, type, nullable, default):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.default = default
