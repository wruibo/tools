'''
    database storage
'''

from spider.storage.cstorage import Storage

from storage.chelper import DBHelper


class DBStorage(Storage):
    def __init__(self, host, user, pwd, dbn, port=3306):
        Storage.__init__(self, dbn)

        # build connection to mysql
        self.dbc = DBHelper.connect_database(host, user, pwd, port)

        # create database if not exist
        if not DBHelper.has_database(self.dbc, dbn):
            DBHelper.create_database(dbn)

        # use the specified database
        DBHelper.use_database(self.dbc, dbn)

    def __del__(self):
        #close database connection
        if self.dbc is not None:
            self.dbc.close()

    def create(self, table):
        if not DBHelper.has_table(self.dbc, table.name):
            DBHelper.create_table(self.dbc, table)
        else:
            DBHelper.update_table(self.dbc, table)

    def getall(self, table):
        pass

    def insert(self, record):
        pass

    def update(self, record):
        pass


if __name__ == "__main__":
    from storage.cfield import *
    from storage.ctable import *

    storage = DBStorage("localhost", "root", "root", "db_spider")

    table = Table("tb_link", storage)
    table.field("id", Type.Int(), False, Value.AutoInc())
    table.field("url", Type.String(512), False)
    table.field("ref", Type.String(512), True)
    table.field("code", Type.String(32), False)
    table.field("fetched", Type.Boolean(), True)
    table.field("fetch_time", Type.BigInt(), True)

    table.key(Key.PrimaryKey, "pk_id", "id")

    table.index(Index.UniqueIndex, "index_url", "url")

    table.create()
