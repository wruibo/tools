
class Key:
    def __init__(self):
        pass

    class Base:
        def __init__(self, name, *fields):
            self.name = name
            self.fields = list(fields)

    class NormalKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)

    class UniqueKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)

    class PrimaryKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)