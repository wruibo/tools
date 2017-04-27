'''
    database storage
'''

from storage.chelper import DBHelper, Wrapper
from storage.cstorage import Storage


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

    def drop(self, table):
        DBHelper.drop_table(self.dbc, table)

    def truncate(self, table):
        DBHelper.truncate_table(self.dbc, table)

    def getall(self, table):
        ntable = table.name
        nfields = table.nfields()

        sql = "select %s from %s" % (",".join(nfields), ntable)
        return DBHelper.select(self.dbc, sql)

    def insert(self, table, records):
        if not isinstance(records, list):
            records = [records]

        ntable = table.name
        nfields = table.nfields()
        values = []
        for record in records:
            if table.match(record):
                value = []
                for nfield in nfields:
                    value.append(Wrapper.wrap(record.get(nfield)))
                values.append(",".join(value))

        if len(values) > 0:
            nfields = ",".join(nfields)
            values = "),(".join(values)
            sql = "insert into %s(%s) values(%s);" % (ntable, nfields, values)
            DBHelper.insert(self.dbc, sql)

if __name__ == "__main__":
    from storage.ctable import *
    from storage.crecord import *

    storage = DBStorage("localhost", "root", "root", "db_spider")
    table = DemoTable()
    table.create(storage)
    table.truncate()

    table.insert(DemoRecord.random_records(10))

    for record in table.getall(DemoRecord):
        print record

