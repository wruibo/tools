'''
    key schema
'''
import re


class Key:
    def __init__(self, type=None, name=None, *fields):
        self.type = type
        self.name = name
        self.fields = list(fields)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
           return self.name == other.name and self.fields == other.fields

        return False

    def tosql(self):
        return "%s %s(%s)" % (self.type, self.name, ",".join(self.fields))

    def fromsql(self, sql):
        sql = sql.strip()

        regex_key = re.compile(r'(?P<type>(unique|primary)?)'
                               r'(?P<key>key)'
                               r'(`)?'
                               r'(?P<name>[\w_]+)'
                               r'(`)?'
                               r'\('
                               r'(?P<fields>[`\w,\s]+)'
                               r'\)',
                               re.IGNORECASE)

        mobj = regex_key.match(sql)
        if mobj:
            type, key, name, fields = mobj.group('type', 'key', 'name', 'fields')
            pass

    def tostr(self):
        return "class=%s;name=%s;fields=%s" % (self.__class__.__name__, self.name, ",".join(self.fields))

    def fromstr(self, str):
        KeyCls = {NormalKey.__name__: NormalKey, UniqueKey.__name__: UniqueKey, PrimaryKey.__name__: PrimaryKey}
        regex_key = re.compile(r'^\s*class\s*=\s*(?P<class>[\w]+)\s*;\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*fields\s*=\s*(?P<fields>[\w,]+)\s*$')
        mobj = regex_key.match(str)
        if mobj:
            cls, name, strfields = mobj.group('class', 'name', 'fields')

            fields = []
            for field in strfields.split(','):
                field = field.strip()
                if field:
                    fields.append(field)

            return KeyCls[cls](name, *tuple(fields))

class NormalKey(Key):
    def __init__(self, name, *fields):
        Key.__init__(self, "key", name, *fields)

class UniqueKey(Key):
    def __init__(self, name, *fields):
        Key.__init__(self, "unique key", name, *fields)

class PrimaryKey(Key):
    def __init__(self, name, *fields):
        Key.__init__(self, "primary key", name, *fields)

if __name__ == "__main__":
    key1 = NormalKey("normal_key", "col1", "col2", "col3")
    key2 = UniqueKey("unique_key", "col1", "col2", "col3")
    key3 = PrimaryKey("primary_key", "col1", "col2", "col3")

    str1 = key1.tostr()
    str2 = key2.tostr()
    str3 = key3.tostr()

    print str1
    print str2
    print str3

    print Key().fromstr(str1).tostr()
    print Key().fromstr(str2).tostr()
    print Key().fromstr(str3).tostr()
