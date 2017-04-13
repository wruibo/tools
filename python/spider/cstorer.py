import sys

import MySQLdb

from clogger import logger
from cpipe import Pipe


class Storer(Pipe):
    def __init__(self):
        pass

    def open(self):
        pass

    def store(self, obj):
        pass

    def update(self, obj):
        pass

    def exist(self, obj):
        pass

    def close(self):
        pass


class DBMysql(Storer):
    def __init__(self, host, user, pwd, dbn, port=3306):
        '''
            init mysql database storer
        :param host: mysql db host
        :param user: mysql db user
        :param pwd: mysql db password for user
        :param dbn:  database name
        :param port:  mysql port
        '''
        Storer.__init__()

        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbn = dbn
        self.port = port

        self.dbc = None
        self.cursor = None

        self.tables = None

    def open(self):
        '''
            open mysql database
        :return:
        '''
        #build connection to mysql
        self.dbc = MySQLdb.connect(host = self.host, user = self.user, passwd = self.pwd, port = self.port)

        #create database if not exist
        if not self._db_exist(self._dbn):
            self._db_create(self._dbn)

        #use the specified database
        self._db_use(self._dbn)

        #get the cursor for query
        self.cursor = self.dbc.cursor()

        #load all tables in database
        self.tables = self._table_all()

    def store(self, obj):
        pass

    def update(self, obj):
        pass

    def exist(self):
        pass

    def close(self):
        if self.db is not None:
            self.db.close()

    def _db_all(self):
        sql = "show databases;"

        dbs = []
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            dbs.append(result[0].lower())

        return dbs

    def _db_exist(self, name):
        name = name.lower()

        dbs = self._db_all()
        for db in dbs:
            if db == name:
                return True

        return False

    def _db_create(self, name):
        sql = "create database if not exist %s default charset utf8 collate utf8_general_ci;" % name

        self.cursor.execute(sql)

    def _db_use(self, name):
        sql = "use %s;" % name

        self.cursor.execute(sql)

    def _table_all(self):
        sql = "show tables;"

        tables = {}
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            name = result[0].lower()
            table = Table.from_desc(self._table_desc(name))
            tables[name] = table

        return tables

    def _table_desc(self, name):

        pass

    def _table_exist(self, name):
        pass

    def _table_create(self):
        pass


class Database:
    def __init__(self, db, name):
        self.db = db
        self.name = name

    def __str__(self):
        pass

    def open(self):
        self.db.use(self.name)

    def create(self, table):
        pass

    def getall(self):
        pass

    def exist(self):
        pass

    def close(self):
        pass


class Table:
    def __init__(self, objclass):
        self.name = ""

    def columns(self, *columns):
        pass

    def create(self):
        pass

    def insert(self, row):
        pass

    def update(self, row):
        pass

    def commit(self):
        pass

    def sql(self):
        pass


class Column:
    def __init__(self, name, type, null = True, default = None):
        self.name = name
        self.type = type
        self.default = default

    def sql(self):
        pass


class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_integer(val):
        pass

    @staticmethod
    def is_float(val):
        pass

class testa:
    def __init__(self):
        pass

    def connect(self):
        print "connect"

def fun(name):
    name = "abc"

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", port=3306)
    cursor = db.cursor()
    cursor.execute("show databases;")
    results = cursor.fetchall()
    for result in results:
        print result

    cursor.execute("use xy;")
    results = cursor.execute("show tables;")
    results = cursor.fetchall()
    for result in results:
        print result

    cursor.execute("truncate tb_test;")

    for i in range(1, 4):
        sql = "insert into tb_test(name) values(%d);" % i
        cursor.execute(sql)
        db.commit()

    cursor1 = db.cursor()

    cursor1.execute("select * from tb_test;")
    result = cursor1.fetchone()
    for i in range(1, 4):
        print result
        result = cursor1.fetchone()

    for i in range(4, 7):
        sql = "insert into tb_test(name) values(%d);" % i
        cursor.execute(sql)
        db.commit()

    result = cursor1.fetchone()
    for i in range(1, 4):
        print result
        result = cursor1.fetchone()

    db.close()


