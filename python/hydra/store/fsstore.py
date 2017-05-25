'''
    file system based database
'''
import threading

from util.path import *
from util.log import Logger
from util.lock import Lock

from store.store import Store
from store.table import Table
from store.fstable import FSTable


class FSStore(Store):
    def __init__(self):
        Store.__init__(self)
        self.path = None #store path
        self.lock = threading.Lock() #lock for operate database table


    def open(self, path):
        '''
            open store or create it if not exist
        :return:
        '''
        try:
            with Lock(self.lock):
                #init store path
                self.path = path

                if not path_exists(self.path):
                    #create database
                    self._create()
                else:
                    # load database
                    self._load()

                self._rebuild_tindex()

                return self
            Logger.info("open store %s...success. %d tables.", self.path, len(self.tables))
        except Exception, e:
            Logger.error("open store %s...failed. error: %s", self.path, str(e))
            raise e

    def close(self):
        '''
            close store
        :return:
        '''
        with Lock(self.lock):
            pass

    def create_table(self, table):
        '''
            create table in current database
        :param table:
        :return:
        '''
        with Lock(self.lock):
            # test if the table has loaded
            for t in self.tables:
                if t.table == table:
                    Logger.info("create table %s...exists.", table.name)
                    return

            #create new table
            table = FSTable().create(self.path, table)

            for i in range(0, len(self.tables)):
                t = self.tables[i]
                if t.table.name == table.name:
                    self.tables.pop(i)
                    break

            self.tables.append(table)

            self._rebuild_tindex()

    def describe_tables(self):
        '''
            describe all table structures
        :return:
        '''
        with Lock(self.lock):
            tables = []
            for table in self.tables:
                tables.append(table.desc())
            return tables

    def drop_table(self, name):
        '''
            drop table in current database
        :param table:
        :return:
        '''
        with Lock(self.lock):
            for table in self.tables:
                if table.name == name:
                    table.drop()
                    self.tables.remove(table)
                    break

        self._rebuild_tindex()

    def drop_tables(self):
        '''
            clear all tables in store
        :return:
        '''
        with Lock(self.lock):
            for table in self.tables:
                table.drop()
            self.tables = []

        self._rebuild_tindex()

    def _create(self):
        '''
            create store directory if not exists
        :return:
        '''
        #create database's root directory
        if not path_exists(self.path):
            make_dirs(self.path)


    def _load(self):
        '''
            load tables in store
        :return:
        '''
        #load tables in store
        for table_name in list_dirs(self.path):
            table = FSTable().load(self.path, table_name)
            self.tables.append(table)

if __name__ == "__main__":
    pass
