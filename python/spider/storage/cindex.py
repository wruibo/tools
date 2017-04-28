'''
    index schema
'''
import re


class Index:
    def __init__(self, table=None, name=None, *fields):
        self.table = table
        self.name = name
        self.fields = list(fields)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
           return self.table==other.table and self.name == other.name and self.fields==other.fields

        return False

    def tostr(self):
        return "class=%s;table=%s;name=%s;fields=%s" % (self.__class__.__name__, self.table, self.name, ",".join(self.fields))

    def fromstr(self, str):
        IndexCls = {NormalIndex.__name__: NormalIndex, UniqueIndex.__name__: UniqueIndex}
        key_regex = re.compile(r'^\s*class\s*=\s*(?P<class>[\w]+)\s*;\s*table\s*=\s*(?P<table>[\w]+)\s*;\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*fields\s*=\s*(?P<fields>[\w,]+)\s*$')
        mobj = key_regex.match(str)
        if mobj:
            cls, table, name, strfields = mobj.group('class', 'table', 'name', 'fields')

            fields = []
            for field in strfields.split(','):
                field = field.strip()
                if field:
                    fields.append(field)

            return  IndexCls[cls](table, name, *tuple(fields))


class NormalIndex(Index):
    def __init__(self, table, name, *fields):
        Index.__init__(self, table, name, *fields)


class UniqueIndex(Index):
    def __init__(self, table, name, *fields):
        Index.__init__(self, table, name, *fields)

if __name__ == "__main__":
    index1 = NormalIndex("table", "normal_key", "col1", "col2", "col3")
    index2 = UniqueIndex("table", "unique_key", "col1", "col2", "col3")

    str1 = index1.tostr()
    str2 = index2.tostr()

    print str1
    print str2

    print Index().fromstr(str1).tostr()
    print Index().fromstr(str2).tostr()
