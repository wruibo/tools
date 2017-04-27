'''
    table for storage
'''
from storage.cschema import Schema


class Table:
    '''
        base table class for storage
    '''
    def __init__(self, name):
        self.name = name
        self.schema = Schema(name)

        self.storage = None

    def storage(self, storage):
        self.storage = storage

    def create(self, storage):
        self.storage = storage
        self.storage.create(self.schema)

    def drop(self):
        self.storage.drop(self.name)

    def truncate(self):
        self.storage.truncate(self.name)

    def getall(self, recordcls):
        return self.storage.getall(self.name, recordcls)

    def insert(self, records):
        return self.storage.insert(self.name, records)


class DemoTable(Table):
    def __init__(self, name="tb_demo"):
        from storage.ckey import *
        from storage.ctype import *
        from storage.cvalue import *
        from storage.cindex import *

        Table.__init__(self, name)

        self.schema.field("id", Type.Int(), False, Value.AutoInc())
        self.schema.field("code", Type.String(32), False, None)
        self.schema.field("name", Type.String(32), True, None)
        self.schema.field("valid", Type.Boolean(), True, None)
        self.schema.field("create_time", Type.BigInt(), True, None)

        self.schema.key(Key.PrimaryKey, "pk_id", "id")
        self.schema.key(Key.NormalKey, "normal_key", "name")
        self.schema.key(Key.UniqueKey, "unique_key", "code")

        self.schema.index(Index.NormalIndex, "normal_index", "name")
        self.schema.index(Index.UniqueIndex, "unique_index", "code")


if __name__ == '__main__':
    pass
    from spider.storage import SQLHelper
#    from storage.cdbstorage import DBStorage

#    storage = DBStorage("localhost", "root", "root", "db_spider")

    table = DemoTable()
    print SQLHelper.sql_create_table(table)
