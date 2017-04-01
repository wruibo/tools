import sys

import MySQLdb


class DBStorer:
    def __init__(self, workdir = "./storer"):
        self.__workdir = workdir
        self.__dbs = {}

    def create(self):
        pass

    def register(self, db):
        pass

    def remove(self, db):
        pass

    def dbs(self):
        return self.__dbs

    def getdb(self, name):
        return self.__dbs.get(name)

    def destroy(self):
        pass


class DBMysql:
    def __init__(self, host, port, user, password, name):
        self.name = ""
        self.tables = {}


class Table:
    def __init__(self):
        self.name = ""

    def __str__(self):
        pass

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


class Row:
    def __init__(self, **kv):
        self.columns = kv

    def __str__(self):
        pass




class Column:
    def __init__(self, name, type, default = None):
        self.name = name
        self.type = type
        self.default = default

    def __str__(self):
        pass

class DBFile:
    def __init__(self):
        pass

    def create(self):
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def commit(self):
        pass

if __name__ == "__init__":
    pass

