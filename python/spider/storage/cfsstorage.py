'''
    file system based database
'''
import threading

from utility.cpath import *
from utility.clog import logger
from utility.clock import clock

from storage.ctable import Table
from storage.cfstable import FSTable
from storage.cstorage import Storage


class FSStorage(Storage):
    def __init__(self):
        Storage.__init__(self)
        self.path = None #storage path
        self.lock = threading.Lock() #lock for operate database table


    def open(self, path):
        '''
            open storage or create it if not exist
        :return:
        '''
        try:
            with clock(self.lock):
                #init storage path
                self.path = path

                if not path_exists(self.path):
                    #create database
                    self._create()
                else:
                    # load database
                    self._load()

                self._rebuild_tindex()

                return self
            logger.info("open storage %s...success. %d tables.", self.path, len(self.tables))
        except Exception, e:
            logger.error("open storage %s...failed. error: %s", self.path, str(e))
            raise e

    def close(self):
        '''
            close storage
        :return:
        '''
        with clock(self.lock):
            pass

    def create_table(self, table):
        '''
            create table in current database
        :param table:
        :return:
        '''
        with clock(self.lock):
            # test if the table has loaded
            for t in self.tables:
                if t.table == table:
                    logger.info("create table %s...exists.", table.name)
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
        with clock(self.lock):
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
        with clock(self.lock):
            for table in self.tables:
                if table.name == name:
                    table.drop()
                    self.tables.remove(table)
                    break

        self._rebuild_tindex()

    def drop_tables(self):
        '''
            clear all tables in storage
        :return:
        '''
        with clock(self.lock):
            for table in self.tables:
                table.drop()
            self.tables = []

        self._rebuild_tindex()

    def _create(self):
        '''
            create storage directory if not exists
        :return:
        '''
        #create database's root directory
        if not path_exists(self.path):
            make_dirs(self.path)


    def _load(self):
        '''
            load tables in storage
        :return:
        '''
        #load tables in storage
        for table_name in list_dirs(self.path):
            table = FSTable().load(self.path, table_name)
            self.tables.append(table)

if __name__ == "__main__":
    pass
