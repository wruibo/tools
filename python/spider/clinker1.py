'''
    linker who manage the links to be crawled
'''
from chelper import Helper
from cstorer import Table


class Type:
    def __init__(self):
        pass

    class Base:
        def __init__(self):
            pass

        def sql(self):
            pass

    class Int(Base):
        def __init__(self):
            Type.Base.__init__(self)

        def sql(self):
            return "integer"

    class BigInt(Base):
        def __init__(self):
            Type.Base.__init__(self)

        def sql(self):
            return "bigint"

    class Float(Base):
        def __init__(self):
            Type.Base.__init__(self)

        def sql(self):
            return "float"

    class Decimal(Base):
        def __init__(self, length, precision):
            Type.Base.__init__(self)

            self.length = length
            self.precision = precision

        def sql(self):
            return "decimal(%d, %d)" % (self.length, self.precision)

    class Boolean(Base):
        def __init__(self):
            Type.Base.__init__(self)

        def sql(self):
            return "boolean"

    class String(Base):
        def __init__(self, length):
            Type.Base.__init__(self)

            self.length = length

        def sql(self):
            return "varchar(%d)" % self.length

    class Text(Base):
        def __init__(self):
            Type.Base.__init__(self)

        def sql(self):
            return "text"


class Value:
    def __init__(self):
        pass

    class Base:
        def __init__(self, value):
            self.value = value

    class Null(Base):
        def __init__(self):
            Value.Base.__init__(self, None)

        def sql(self):
            return "null"

    class AutoInc(Base):
        def __init__(self):
            Value.Base.__init__(self, None)

        def sql(self):
            return "auto_increment"

    class Int(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default %d" % self.value
            else:
                return ""

    class BigInt(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default %d" % self.value
            else:
                return ""

    class Float(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default %f" % self.value
            else:
                return ""

    class Decimal(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default %f" % self.value
            else:
                return ""

    class Boolean(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                if self.value:
                    return "default true"
                else:
                    return "default false"
            else:
                return ""

    class String(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default \'%s\'" % self.value
            else:
                return ""

    class Text(Base):
        def __init__(self, value=None):
            Value.Base.__init__(self, value)

        def sql(self):
            if self.value is not None:
                return "default \'%s\'" % self.value
            else:
                return ""


class Key:
    def __init__(self):
        pass

    class Base:
        def __init__(self, name, *columns):
            self.name = name
            self.columns = list(columns)

    class NormalKey(Base):
        def __init__(self, name, *columns):
            Key.Base.__init__(self, name, *columns)

        def sql(self):
            return "\tkey %s(%s)" % (self.name, ",".join(self.columns))

    class UniqueKey(Base):
        def __init__(self, name, *columns):
            Key.Base.__init__(self, name, *columns)

        def sql(self):
            return "\tunique key %s(%s)" % (self.name, ",".join(self.columns))

    class PrimaryKey(Base):
        def __init__(self, name, *columns):
            Key.Base.__init__(self, "pk", *columns)

        def sql(self):
            return "\tprimary key (%s)" % ",".join(self.columns)


class Index:
    def __init__(self):
        pass

    class Base:
        def __init__(self, table, name, *columns):
            self.table = table
            self.name = name
            self.columns = list(columns)

    class NormalIndex(Base):
        def __init__(self, table, name, *columns):
            Index.Base.__init__(self, table, name, *columns)

        def sql(self):
            return "create index %s on %s\n(\n\t%s\n);" % (self.name, self.table, ",\n\t".join(self.columns))

    class UniqueIndex(Base):
        def __init__(self, table, name, *columns):
            Index.Base.__init__(self, table, name, *columns)

        def sql(self):
            return "create unique index %s on %s\n(\n\t%s\n);" % (self.name, self.table, ",\n\t".join(self.columns))


class Column:
    def __init__(self, name, type, nullable, default):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.default = default

    def default(self):
        if self.default is not None:
            return self.default.value()
        else:
            return None

    def sql(self):
        if self.nullable:
            return "\t%s %s default null" % (self.name, self.type.sql())
        else:
            if self.default is not None:
                return "\t%s %s not null %s" % (self.name, self.type.sql(), self.default.sql())
            else:
                return "\t%s %s not null" % (self.name, self.type.sql())


class Table:
    def __init__(self, name):
        self.name = name

        self.columns = []
        self.keys = []
        self.indexs = []

    def insert(self, item):
        pass

    def update(self, item):
        pass

    def column(self, name, type = None, nullable = None, default=None):
        if type is not None:
            if not hasattr(self, name):
                if default is not None:
                    setattr(self, name, default.value)
                else:
                    setattr(self, name, None)

            self.columns.append(Column(name, type, nullable, default))
        else:
            for column in self.columns:
                if name == column.name:
                    return column

            return None


    def key(self, typecls, name, *columns):
        self.keys.append(typecls(name, *columns))

    def index(self, typecls, name, *columns):
        self.indexs.append(typecls(self.name, name, *columns))

    def sql(self):
        columns = self._sql_columns()
        keys = self._sql_keys()
        indexs = self._sql_indexs()

        if keys != "":
            columns = "%s%s" % (columns, ",\n")

        return "create table %s\n(\n%s%s\n);\n\n%s" % (self.name, columns, keys, indexs)

    def _sql_columns(self):
        columns = []
        for column in self.columns:
            columns.append(column.sql())
        return ",\n".join(columns)

    def _sql_keys(self):
        keys = []
        for key in self.keys:
            keys.append(key.sql())
        return ",\n".join(keys)

    def _sql_indexs(self):
        indexs = []
        for index in self.indexs:
            indexs.append(index.sql())
        return "\n\n".join(indexs)


class Item:
    def __init__(self, table, item):
        self.table = table
        self.item = item


class Link1:
    TABLE_NAME = "tb_link"

    def __init__(self):
        pass

    class Table(Table):
        def __init__(self):
            Table.__init__(self, Link.TABLE_NAME)

            self.column("id", Type.Int(), False, Value.AutoInc())
            self.column("url", Type.String(512), False)
            self.column("ref", Type.String(512), True)
            self.column("fetched", Type.Boolean(), True)
            self.column("fetch_time", Type.BigInt(), True)

            self.key(Key.PrimaryKey, "pk_id", "id")

    class Item(Item):
        def __init__(self):
            Item.__init__(self, Link.Table())

            self.id = self.table.column("id").default()
            self.url = self.table.column("url").default()
            self.ref = self.table.column("ref").default()
            self.fetched = self.table.column("fetched").default()
            self.fetch_time = self.table.column("access_time").default()


class Link:
    def __init__(self, url, ref=None):
        self.id = Helper.md5(url)
        self.url = url
        self.ref = ref
        self.fetched = False
        self.fetch_time = None


class Linker(Pipe):
    def __init__(self):
        Pipe.__init__(self)

        self.links = []
        self.indexs = {}
        self.pos = 0

    def __del__(self):
        pass

    def feed(self, link):
        if not isinstance(link, Link):
            return

        if not self.indexs.has_key(link.id):
            self.links.append(link)
            self.indexs[link.id] = len(self.links)

    def fetch(self):
        if self.pos == len(self.links):
            return None

        link = self.links[self.pos]
        self.pos += 1

        return link


if __name__ == "__main__":
    link_table = Link.Table()
    print(link_table.sql())
    print(link_table.id)
