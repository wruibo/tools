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
        self.path = None #storage path
        self.tables = [] #file system tables
        self.lock = threading.Lock() #database lock


    def open(self, path):
        '''
            open storage or create it if not exist
        :return:
        '''
        with clock(self.lock):
            #init storage path
            self.path = path

            if not path_exists(self.path):
                #create database
                self._create()
            else:
                # load database
                self._load()

            return self

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
            if self._table_loaded(table):
                logger.info("create table %s...exists.", table.name)
            else:
                #create new table
                table = FSTable().create(self.path, table)
                self.tables.append(table)

    def drop_table(self, table):
        '''
            drop table in current database
        :param table:
        :return:
        '''
        table_name = self._table_name(table)

        with clock(self.lock):
            for table in self.tables:
                if table.name==table:
                    table.drop()
                    self.tables.remove(table)


    def truncate_table(self, table):
        '''
            truncate table data
        :param table:
        :return:
        '''
        table_name = self._table_name(table)

        with clock(self.lock):
            for table in self.tables:
                if table.name==table_name:
                    table.truncate()

    def select_from_table(self, table):
        '''
            select all records from table
        :param table:
        :return:
        '''
        table_name = self._table_name(table)

        with clock(self.lock):
            for table in self.tables:
                if table.name==table_name:
                    return table.select()

    def insert_into_table(self, table, models):
        '''
            insert records into table
        :param table:
        :param models:
        :return:
        '''
        table_name = self._table_name(table)

        with clock(self.lock):
            for table in self.tables:
                if table.name == table_name:
                    table.insert(models)

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
            table = FStable().load(self.path, table_name)
            self.tables.append(table)

    def _table_loaded(self, table):
        '''
            test if table(schema) has loaded
        :param table:
        :return:
        '''
        for t in self.tables:
            if t.table == table:
                return True

        return False

    def _table_name(self, table):
        table_name = table
        if issubclass(table.__class__, Table):
            table_name = table.name
        return table_name

if __name__ == "__main__":
    storage = FSStorage().open("./database")

    from storage.ctable import DemoTable

    table = DemoTable()
    storage.create_table(table)

    from storage.cmodel import DemoModel

    storage.insert_into_table(table, DemoModel().randoms(5))

    print storage.select_from_table(table)
