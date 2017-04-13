from spider.storage.cunit import *


class DBKey:
    def __init__(self):
        pass

    class Base:
        def __init__(self, name, *columns):
            self.name = name
            self.columns = list(columns)

    class NormalKey(Base):
        def __init__(self, name, *columns):
            DBKey.Base.__init__(self, name, *columns)

        def sql(self):
            return "\tkey %s(%s)" % (self.name, ",".join(self.columns))

    class UniqueKey(Base):
        def __init__(self, name, *columns):
            DBKey.Base.__init__(self, name, *columns)

        def sql(self):
            return "\tunique key %s(%s)" % (self.name, ",".join(self.columns))

    class PrimaryKey(Base):
        def __init__(self, name, *columns):
            DBKey.Base.__init__(self, "pk", *columns)

        def sql(self):
            return "\tprimary key (%s)" % ",".join(self.columns)


class DBIndex:
    def __init__(self):
        pass

    class Base:
        def __init__(self, table, name, *columns):
            self.table = table
            self.name = name
            self.columns = list(columns)

    class NormalIndex(Base):
        def __init__(self, table, name, *columns):
            DBIndex.Base.__init__(self, table, name, *columns)

        def sql(self):
            return "create index %s on %s\n(\n\t%s\n);" % (self.name, self.table, ",\n\t".join(self.columns))

    class UniqueIndex(Base):
        def __init__(self, table, name, *columns):
            DBIndex.Base.__init__(self, table, name, *columns)

        def sql(self):
            return "create unique index %s on %s\n(\n\t%s\n);" % (self.name, self.table, ",\n\t".join(self.columns))


class DBColumn(Column):
    def __init__(self, name, type, nullable, default):
        Column.__init__(self, name, type, nullable, default)

    def sql(self):
        if self.nullable:
            return "\t%s %s default null" % (self.name, SQLHelper.sqlfromtype(self.type))
        else:
            if self.default is not None:
                return "\t%s %s not null %s" % (self.name, SQLHelper.sqlfromtype(self.type), SQLHelper.sqlfromdefault(self.default))
            else:
                return "\t%s %s not null" % (self.name, SQLHelper.sqlfromtype(self.type))


class DBTable(Table):
    def __init__(self, name):
        Table.__init__(self, name)

        self.keys = []
        self.indexs = []

    def column(self, name, type = None, nullable = None, default=None):
        if type is not None:
            self.columns.append(DBColumn(name, type, nullable, default))
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


class SQLHelper:
    def __init__(self):
        pass

    @staticmethod
    def sqlfromtype(type):
        if isinstance(type, Type.Int):
            return "integer"
        elif isinstance(type, Type.BigInt):
            return "bigint"
        elif isinstance(type, Type.Float):
            return "float"
        elif isinstance(type, Type.Decimal):
            return "decimal(%d,%d)" % (type.length, type.precision)
        elif isinstance(type, Type.Boolean):
            return "boolean"
        elif isinstance(type, Type.String):
            return "varchar(%d)" % type.length
        elif isinstance(type, Type.Text):
            return "text"
        else:
            raise TypeError("unsupport column type: %s" % type.__class__.__name__)

    @staticmethod
    def sqlfromdefault(value):
        if isinstance(value, Value.Null):
            return "default null"
        elif isinstance(value, Value.AutoInc):
            return "auto_increment"
        elif isinstance(value, Value.Boolean):
            return "default %s" % str(value.value).lower()
        elif isinstance(value, Value.Int) or isinstance(value, Value.BigInt):
            return "default %d" % value.value
        elif isinstance(value, Value.Float) or isinstance(value, Value.Decimal):
            return "default %f" % value.value
        elif isinstance(value, Value.String) or isinstance(value, Value.Text):
            return "default \'%s\'" % value.value
        else:
            ""


if __name__ == '__main__':
    table = DBTable("tb_link")
    table.column("id", Type.Int(), False, Value.AutoInc())
    table.column("url", Type.String(512), False)
    table.column("ref", Type.String(512), True)
    table.column("fetched", Type.Boolean(), True)
    table.column("fetch_time", Type.BigInt(), True)

    table.key(DBKey.PrimaryKey, "pk_id", "id")

    table.key(DBKey.NormalKey, "normal_key", "id", "url")
    table.key(DBKey.UniqueKey, "unique_key", "url", "ref")

    table.index(DBIndex.NormalIndex, "normal_index", "id", "url")
    table.index(DBIndex.UniqueIndex, "unique_index", "id", "url")

    print table.sql()
