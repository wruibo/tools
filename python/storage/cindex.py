
class Index:
    def __init__(self):
        pass

    class Base:
        def __init__(self, table, name, *fields):
            self.table = table
            self.name = name
            self.fields = list(fields)

    class NormalIndex(Base):
        def __init__(self, table, name, *fields):
            Index.Base.__init__(self, table, name, *fields)

    class UniqueIndex(Base):
        def __init__(self, table, name, *fields):
            Index.Base.__init__(self, table, name, *fields)
