'''
    database store
'''
import MySQLdb

from util.log import Logger
from store.store import Store
from store.dbtable import DBTable


class DBStore(Store):
    def __init__(self):
        Store.__init__(self)

        self.host = None
        self.port = None
        self.user = None
        self.pwd = None

        self.dbn = None # database name
        self.dbc = None #database connection

    def open(self, host, user, pwd, dbn, port=3306):
        '''
            open database or create it if not exist
        :return:
        '''
        #init store path
        try:
            self.host, self.port, self.user, self.pwd = host, port, user, pwd
            self.dbn = dbn
            self.dbc = MySQLdb.connect(host=host, user=user, passwd=pwd, port=port)

            if not self._exists():
                #create database
                self._create()
                self._use()
            else:
                # load database
                self._use()
                self._load()

            self._rebuild_tindex()

            return self
            Logger.info("open store mysql://%s:%s@%s:%d/%s...success. %d tables.", user, pwd, host, port, self.dbn, len(self.tables))
        except Exception, e:
            Logger.error("open store mysql://%s:%s@%s:%d/%s...failed. error: %s", user, pwd, host, port, self.dbn, str(e))
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
            Logger.info("close store mysql://%s:%s@%s:%d/%s...success.", self.user, self.pwd, self.host, self.port, self.dbn)
        except Exception, e:
            Logger.info("close store mysql://%s:%s@%s:%d/%s...failed. error: %s", self.user, self.pwd, self.host, self.port, self.dbn, str(e))
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
                Logger.info("create table %s...exists.", table.name)
                return

        #create new tabel if not exists or changed
        dbtable = DBTable().create(self.dbc, table)

        for i in range(0, len(self.tables)):
            t = self.tables[i]
            if t.table.name == table.name:
                self.tables.pop(i)
                break

        self.tables.append(dbtable)

        self._rebuild_tindex()

    def describe_tables(self):
        '''
            describe all table structures
        :return:
        '''
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
        for table in self.tables:
            if table.name == name:
                table.drop()
                self.tables.remove(table)

        self._rebuild_tindex()

    def drop_tables(self):
        '''
            clear all tables in store
        :return:
        '''
        for table in self.tables:
            table.drop()
        self.tables = []

        self._rebuild_tindex()

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
            create store directory if not exists
        :return:
        '''
        #create database's root directory
        sql = "create database if not exists %s default charset utf8 collate utf8_general_ci;" % self.dbn
        self.dbc.cursor().execute(sql)


    def _load(self):
        '''
            load tables in store
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
        sql = "use %s;" % self.dbn
        self.dbc.cursor().execute(sql)


if __name__ == "__main__":
    pass

