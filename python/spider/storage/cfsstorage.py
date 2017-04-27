'''
    file system storage
'''
from utility.cpath import cpath
from storage.chelper import FSHelper
from storage.cstorage import Storage
from storage.cfstable import FStable
from storage.cfsdatabase import FSDatabase


class FSStorage(Storage):
    def __init__(self, path, name):
        Storage.__init__(self, name)

        self.db = FSDatabase(cpath.join(path, name))

    def create(self, table_schema):
        self.db.create_table(table_schema)

    def drop(self, table_name):
        self.db.drop_table(table_name)

    def truncate(self, table_name):
        self.db.truncate_table(table_name)

    def getall(self, table_name):
        self.db.select_from_table(table_name)

    def insert(self, table_name, records):
        self.db.insert_into_table(table_name, records)


if __name__ == "__main__":
    pass
