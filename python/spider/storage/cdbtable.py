'''
    file system table
'''

from utility.cstr import *
from utility.cpath import *
from utility.clog import logger


from storage.ckey import *
from storage.ctype import *
from storage.cvalue import *
from storage.cfield import *
from storage.ctable import *
from storage.cverifier import *

FSTableOperationError = Exception


class DBTable:
    '''
        table base on file
    '''
    def __init__(self):
        self.dbc = None #database connection
        self.name = None #table name
        self.table = None #table structure

    def create(self, dbc, table):
        '''
            create table
        :return self
        '''
        try:
            #initialize table parameters
            self.dbc = dbc
            self.name = table.name
            self.table = table

            #check if table has exists
            if self._exists():
                self._update()
            else:
                self._create()

            logger.info("create table %s...success.", self.name)
            return self
        except Exception, e:
            logger.error("create table %s...failed. error: %s", self.name, str(e))
            raise e

    def load(self, dbc, name):
        '''
            load table from database
        :return:  self or None
        '''
        try:
            #initialize table parameters
            self.dbc = dbc
            self.name = name

            #create table structure
            sql = "show create table %s;" % self.name
            cursor = self.dbc.cursor()
            cursor.execute(sql)
            create_sql = cursor.fetchall()[0][0]

            self.table = Table().fromsql(create_sql)

            logger.info("loading table %s...success.", self.name)
            return self
        except Exception, e:
            logger.info("loading table %s...failed. error: %s", self.name, str(e))
            raise e

    def drop(self):
        '''
            drop table
        :return:
        '''
        try:
            sql = "drop table if exists %s;" % self.name
            self.dbc.cursor().execute(sql)
            logger.info("drop table %s...success", self.name)
        except Exception, e:
            logger.error("drop table %s...failed. error %s", self.name, str(e))
            raise e

    def truncate(self):
        '''
            truncate table
        :return:
        '''
        try:
            sql = "truncate table %s;" % table.name
            self.dbc.cursor().execute(sql)
            logger.info("truncate table %s...success", self.name)
        except Exception, e:
            logger.error("truncate table %s...failed. error %s", self.name, str(e))
            raise e

    def select(self):
        '''
            select all data from table
        :return:
        '''
        try:
           nfields = self.table.nfields()
           sql, models = "select %s from %s;" % (",".join(nfields), self.name), []
           cursor = self.dbc.cursor()
           cursor.execute(sql)
           results = cursor.fetchall()
           for result in results:
               model = {}
               for idx in range(0, len(result)):
                   model[nfields[idx]] = result[idx]
               models.append(model)
           logger.info("select from table %s...success", self.name)
           return models

        except Exception, e:
           logger.error("select from table %s...failed. error %s", self.name, str(e))
           raise e


    def insert(self, models):
        '''
            insert data to table
        :param models:
        :return:
        '''
        try:
            nfields, values = self.table.nfields(), []
            for model in models:
                value = []
                for nfield in nfields:
                    value.append(model.get(nfield))
                values.append("(%s)" % ",".join(values))

            sql = "insert into %s(%s) values %s;" % (self.name, ",".join(nfields), "".join(values))
            self.dbc.cursor().execute(sql)

            logger.info("insert into table %s...success", self.name)
        except Exception, e:
            logger.error("insert into table %s...failed. error %s", self.name, str(e))
            raise e


    def _create(self):
        '''
            create table in database
        :return:
        '''
        sql = self.table.tosql()
        self.dbc.cursor().execute(sql)

    def _update(self):
        '''
            update table in database
        :return:
        '''

        after_column = None
        columns = self._nfields()
        for field in self.table.fields:
            if not (field.name in columns):
                if after_column is not None:
                    sql = "alter table %s add column %s after %s" % (self.table.name, field.tosql(), after_column)
                else:
                    sql = "alter table %s add column %s;" % (self.table.name, field.tosql())
                self.dbc.cursor().execute(sql)
            after_column = field.name

    def _exists(self):
        '''
            test if table has exist
        :return:
        '''
        sql, tables = "show tables;", []

        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            tables.append(result[0].lower())

        if self.name.lower() in tables:
            return True

        return False

    def _nfields(self):
        '''
            get table field names in database
        :return:
        '''
        #get nfields on table
        sql, nfields = "desc %s;" % self.name, []
        cursor = self.dbc.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            nfields.append(result[0])

        return nfields


if __name__ == "__main__":
    table = Table("tb_demo")
    table.field("id", Int(), False, AutoIncValue())
    table.field("code", String(32), False, StringValue("123"))
    table.field("name", String(32), True)
    table.field("valid", Boolean(), True)
    table.field("create_time", BigInt(), True)

    table.key(PrimaryKey, "pk_id", "id")
    table.key(NormalKey, "normal_key", "name","code")
    table.key(UniqueKey, "unique_key", "code", "valid")

    from storage.chelper import SQLHelper
    print SQLHelper.sql_create_table(table)
