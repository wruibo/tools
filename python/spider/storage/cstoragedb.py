'''
    database storage
'''
import MySQLdb

from spider.storage.cstorage import Storage


class DBStorage(Storage):
    def __init__(self, host, user, pwd, dbn, port=3306):
        Storage.__init__(self)

        self.helper = DBHelper(host, user, pwd, dbn, port)

    def create(self, table):
        if not self.helper.has_table(table.name):
            self.helper.create_table(table.sql())
        else:
            after_column = None
            columns = self.helper.desc_table(table.name, True)
            for column in table.columns:
                if not column.name in columns:
                    if after_column is not None:
                        sql = "alter table %s add column %s after %s" % (table.name, column.sql(), after_column)
                    else:
                        sql = "alter table %s add column %s;" % (table.name, column.sql())

                    print sql

                    self.helper.execute_sql(sql)

                after_column = column.name


class DBHelper:
    def __init__(self, host, user, pwd, dbn, port=3306):
        #save database connection infomation
        self.host, self.user, self.pwd, self.dbn, self.port = host, user, pwd, dbn, port

        # build connection to mysql
        self.dbc = self.connect_database(host, user, pwd, port)

        # create database if not exist
        if not self.has_database(dbn):
            self.create_database(dbn)

        # use the specified database
        self.use_database(dbn)

    def __del__(self):
        self.dbc.close()

    @staticmethod
    def connect_database(host, user, pwd, port=3306):
        return MySQLdb.connect(host=host, user=user, passwd=pwd, port=port)

    def execute_sql(self, sql):
        return self.dbc.cursor().execute(sql)

    def show_databases(self):
        sql, dbs = "show databases;", []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            dbs.append(result[0].lower())

        return dbs

    def create_database(self, name):
        sql = "create database if not exists %s default charset utf8 collate utf8_general_ci;" % name
        cursor = self.dbc.cursor().execute(sql)

    def use_database(self, name):
        sql = "use %s;" % name
        self.dbc.cursor().execute(sql)

    def has_database(self, name):
        return name.lower() in self.show_databases()

    def show_tables(self):
        sql, tables = "show tables;", []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            tables.append(result[0].lower())

        return tables

    def create_table(self, sql):
        self.dbc.cursor().execute(sql)

    def has_table(self, name):
        return name.lower() in self.show_tables()

    def desc_table(self, name, onlyname=False):
        sql, columns = "desc %s;" % name, []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            if onlyname:
                columns.append(result[0])
            else:
                columns.append({"field":result[0], "type":result[1], "null":result[2], "key":result[3], "default":result[4], "extra":result[5]})

        return columns

if __name__ == "__main__":
    from spider.storage.cunit import *

    storage = DBStorage("localhost", "root", "root", "db_spider")

    table = DBTable("tb_link")
    table.column("id", Type.Int(), False, Value.AutoInc())
    table.column("url", Type.String(512), False)
    table.column("ref", Type.String(512), True)
    table.column("code", Type.String(32), False)
    table.column("fetched", Type.Boolean(), True)
    table.column("fetch_time", Type.BigInt(), True)

    table.key(DBKey.PrimaryKey, "pk_id", "id")

    print table.sql()

    storage.create(table)