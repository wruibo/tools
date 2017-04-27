import MySQLdb
from storage.cfield import *
from storage.ckey import *
from storage.ctype import *

from storage.cindex import *


class SQLHelper:
    def __init__(self):
        pass

    @staticmethod
    def sql_type(field):
        type = field.type
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
    def sql_default(field):
        value = field.default
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
            return ""

    @staticmethod
    def sql_key(key):
        if isinstance(key, Key.NormalKey):
            return "\tkey %s(%s)" % (key.name, ",".join(key.fields))
        elif isinstance(key, Key.UniqueKey):
            return "\tunique key %s(%s)" % (key.name, ",".join(key.fields))
        elif isinstance(key, Key.PrimaryKey):
            return "\tprimary key (%s)" % ",".join(key.fields)
        else:
            return ""

    @staticmethod
    def sql_index(index):
        if isinstance(index, Index.NormalIndex):
            return "create index %s on %s\n(\n\t%s\n);" % (index.name, index.table, ",\n\t".join(index.fields))
        elif isinstance(index, Index.UniqueIndex):
            return "create unique index %s on %s\n(\n\t%s\n);" % (index.name, index.table, ",\n\t".join(index.fields))
        else:
            return ""

    @staticmethod
    def sql_field(field):
        if field.nullable:
            return "\t%s %s default null" % (field.name, SQLHelper.sql_type(field))
        else:
            if field.default is not None:
                return "\t%s %s not null %s" % (field.name, SQLHelper.sql_type(field), SQLHelper.sql_default(field))
            else:
                return "\t%s %s not null" % (field.name, SQLHelper.sql_type(field))

    @staticmethod
    def sql_create_fields(fields):
        sqls = []
        for field in fields:
            sqls.append(SQLHelper.sql_field(field))
        return ",\n".join(sqls)

    @staticmethod
    def sql_create_keys(keys):
        sqls = []
        for key in keys:
            sqls.append(SQLHelper.sql_key(key))
        return ",\n".join(sqls)

    @staticmethod
    def sql_create_indexs(indexs):
        sqls = []
        for index in indexs:
            sqls.append(SQLHelper.sql_index(index))
        return "\n\n".join(sqls)

    @staticmethod
    def sql_create_table(table):
        name = table.name
        fields = SQLHelper.sql_create_fields(table.fields)
        keys = SQLHelper.sql_create_keys(table.keys)
        indexs = SQLHelper.sql_create_indexs(table.indexs)

        if keys != "":
            fields = "%s%s" % (fields, ",\n")

        return "create table %s\n(\n%s%s\n);\n\n%s" % (name, fields, keys, indexs)


class DBHelper:
    def __init__(self):
        pass

    @staticmethod
    def connect_database(host, user, pwd, port=3306):
        return MySQLdb.connect(host=host, user=user, passwd=pwd, port=port)

    @staticmethod
    def show_databases(dbc):
        sql, dbs = "show databases;", []

        cursor = dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            dbs.append(result[0].lower())

        return dbs

    @staticmethod
    def create_database(dbc, name):
        sql = "create database if not exists %s default charset utf8 collate utf8_general_ci;" % name
        cursor = dbc.cursor().execute(sql)

    @staticmethod
    def use_database(dbc, name):
        sql = "use %s;" % name
        dbc.cursor().execute(sql)

    @staticmethod
    def has_database(dbc, name):
        return name.lower() in DBHelper.show_databases(dbc)

    @staticmethod
    def show_tables(dbc):
        sql, tables = "show tables;", []

        cursor = dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            tables.append(result[0].lower())

        return tables

    @staticmethod
    def create_table(dbc, table):
        sql = SQLHelper.sql_create_table(table)
        dbc.cursor().execute(sql)

    @staticmethod
    def drop_table(dbc, table):
        sql = "drop table if exists %s;" % table.name
        DBHelper.execute(dbc, sql)

    @staticmethod
    def truncate_table(dbc, table):
        sql = "truncate table %s;" % table.name
        DBHelper.execute(dbc, sql)

    @staticmethod
    def update_table(dbc, table):
        after_column = None
        columns = DBHelper.desc_table(dbc, table.name, True)
        for field in table.fields:
            if not (field.name in columns):
                if after_column is not None:
                    sql = "alter table %s add column %s after %s" % (table.name, SQLHelper.sql_field(field), after_column)
                else:
                    sql = "alter table %s add column %s;" % (table.name, SQLHelper.sql_field(field))
                dbc.cursor().execute(sql)
            after_column = field.name

    @staticmethod
    def has_table(dbc, name):
        return name.lower() in DBHelper.show_tables(dbc)

    @staticmethod
    def desc_table(dbc, name, onlyname=False):
        sql, columns = "desc %s;" % name, []

        cursor = dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            if onlyname:
                columns.append(result[0])
            else:
                columns.append({"field":result[0], "type":result[1], "null":result[2], "key":result[3], "default":result[4], "extra":result[5]})

        return columns

    @staticmethod
    def execute(dbc, sql):
        cursor = dbc.cursor()
        cursor.execute(sql)

    @staticmethod
    def insert(dbc, sql):
        cursor = dbc.cursor()
        cursor.execute(sql)
        dbc.commit()

    @staticmethod
    def select(dbc, sql):
        cursor = dbc.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


from utility.cdir import *
from utility.cpath import *


class FSHelper:
    def __init__(self):
        pass

    @staticmethod
    def has_database(path):
        return cpath.exists(path)

    @staticmethod
    def create_database(path):
        if not cpath.exists(path):
            cdir.makes(path)

    @staticmethod
    def has_table(table):
        pass

    @staticmethod
    def create_table(table):
        pass

    @staticmethod
    def update_table(table):
        pass

    @staticmethod
    def drop_table(table):
        pass

    @staticmethod
    def truncate_table(table):
        pass


class Wrapper:
    def __init__(self):
        pass

    @staticmethod
    def wrap(value):
        ntype = value.__class__.__name__
        return TYPE_WRAPPER[ntype](value)

    @staticmethod
    def _wrap_num(value):
        return str(value)

    @staticmethod
    def _wrap_str(value):
        return "\'%s\'" % value

    @staticmethod
    def _wrap_bool(value):
        if value:
            return 'true'
        else:
            return 'false'

    @staticmethod
    def _wrap_none(value):
        return 'null'

TYPE_WRAPPER = {
    'int': Wrapper._wrap_num,
    'float': Wrapper._wrap_num,
    'str': Wrapper._wrap_str,
    'bool': Wrapper._wrap_bool,
    'NoneType':Wrapper._wrap_none
}


if __name__ == "__main__":
    print Wrapper.wrap(1)
    print Wrapper.wrap(1.1)
    print Wrapper.wrap("abc")
    print Wrapper.wrap(None)

