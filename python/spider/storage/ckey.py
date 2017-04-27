'''
    key schema
'''


class Key:
    def __init__(self):
        pass

    class Base:
        def __init__(self, name, *fields):
            self.name = name
            self.fields = list(fields)

        def tostr(self):
            return "class=%s;name=%s;fields=%s" % (self.__class__.__name__, self.name, ",".join(self.fields))

    class NormalKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)

    class UniqueKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)

    class PrimaryKey(Base):
        def __init__(self, name, *fields):
            Key.Base.__init__(self, name, *fields)

    KeyCls = {NormalKey.__name__:NormalKey, UniqueKey.__name__:UniqueKey, PrimaryKey.__name__:PrimaryKey}

    @staticmethod
    def fromstr(str):
        import re
        key_regex = re.compile(r'^\s*class\s*=\s*(?P<class>[\w]+)\s*;\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*fields\s*=\s*(?P<fields>[\w,]+)\s*$')
        mobj = key_regex.match(str)
        if mobj:
            cls, name, strfields = mobj.group('class', 'name', 'fields')

            fields = []
            for field in strfields.split(','):
                field = field.strip()
                if field:
                    fields.append(field)

            return Key.KeyCls[cls](name, *tuple(fields))


if __name__ == "__main__":
    key1 = Key.NormalKey("normal_key", "col1", "col2", "col3")
    key2 = Key.UniqueKey("unique_key", "col1", "col2", "col3")
    key3 = Key.PrimaryKey("primary_key", "col1", "col2", "col3")

    str1 = key1.tostr()
    str2 = key2.tostr()
    str3 = key3.tostr()

    print str1
    print str2
    print str3

    print Key.fromstr(str1).tostr()
    print Key.fromstr(str2).tostr()
    print Key.fromstr(str3).tostr()
