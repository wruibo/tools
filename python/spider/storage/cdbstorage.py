'''
    database storage
'''
import MySQLdb

from utility.clog import logger
from storage.cdbtable import DBTable
from storage.cstorage import Storage


class DBStorage(Storage):
    def __init__(self):
        Storage.__init__(self)

        self.host = None
        self.port = None
        self.user = None
        self.pwd = None

        self.dbn = None # database name
        self.dbc = None #database connection

        self.tables = []

    def open(self, host, user, pwd, dbn, port=3306):
        '''
            open database or create it if not exist
        :return:
        '''
        #init storage path
        try:
            self.host, self.port, self.user, self.pwd = host, port, user, pwd
            self.dbn = dbn
            self.dbc = MySQLdb.connect(host=host, user=user, passwd=pwd, port=port)

            if not self._exists():
                #create database
                self._create()
            else:
                # load database
                self._load()

            self._use()

            return self
            logger.info("open storage mysql://%s:%s@%s:%d/%s...success. %d tables.", user, passwd, host, port, self.dbn, len(self.tables))
        except Exception, e:
            logger.error("open storage mysql://%s:%s@%s:%d/%s...failed. error: %s", user, passwd, host, port, self.dbn, str(e))
            raise e

    def close(self):
        '''
            close datbase
        :return:
        '''
        #close database connection
        try:
            if self.dbc is not None:
                self.dbc.close()
            logger.info("close storage mysql://%s:%s@%s:%d/%s...success.", self.user, self.passwd, self.host, self.port, self.dbn)
        except Exception, e:
            logger.info("close storage mysql://%s:%s@%s:%d/%s...failed. error: %s", self.user, self.passwd, self.host, self.port, self.dbn, str(e))
            raise e

    def create_table(self, table):
        '''
            create table in current database
        :param table:
        :return:
        '''
        #check if the table has exist
        for t in self.tables:
            if t.table == table:
                logger.info("create table %s...exists.", table.name)
                return

        #create new tabel if not exists or changed
        dbtable = DBTable().create(self.dbc, table)

        for i in range(0, len(self.tables)):
            t = self.tables[i]
            if t.table.name == table.name:
                self.tables.pop(i)
                break

        self.tables.append(dbtable)

    def drop_table(self, table):
        '''
            drop table in current database
        :param table:
        :return:
        '''
        table_name = self._table_name(table)

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
        for table in self.tables:
            if table.name == table_name:
                table.insert(models)

    def _exists(self):
        '''
            test if the database has exists
        :return:
        '''
        sql, dbs = "show databases;", []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            dbs.append(result[0].lower())

        if self.dbn in dbs:
            return True
        return False

    def _create(self):
        '''
            create storage directory if not exists
        :return:
        '''
        #create database's root directory
        sql = "create database if not exists %s default charset utf8 collate utf8_general_ci;" % self.dbn
        self.dbc.cursor().execute(sql)


    def _load(self):
        '''
            load tables in storage
        :return:
        '''
        #get all tables in database
        sql, tables = "show tables in %s;" % self.dbn, []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            tables.append(result[0].lower())

        #load tables in database
        for table_name in tables:
            table = DBTable().load(self.dbc, table_name)
            self.tables.append(table)

    def _use(self):
        '''
            switch connection to current database
        :return:
        '''
        sql = "use %s;" % self.name
        self.dbc.cursor().execute(sql)


    def _table_name(self, table):
        table_name = table
        if issubclass(table.__class__, Table):
            table_name = table.name
        return table_name

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

