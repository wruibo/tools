'''
    file system table
'''

from utility.cstr import *
from utility.cpath import *
from utility.clog import logger
from utility.cutil import is_subset


from storage.ckey import *
from storage.ctype import *
from storage.cvalue import *
from storage.cfield import *
from storage.ctable import *
from storage.citable import *
from storage.cverifier import *

FSTableOperationError = Exception


class DBTable(ITable):
    '''
        table base on file
    '''
    def __init__(self):
        self.dbc = None #database connection

    def create(self, dbc, table):
        '''
            create table
        :return self
        '''
        try:
            #initialize table parameters
            self.dbc = dbc
            self.table = table
            self.name = table.name

            #check if table has exists
            if self._exists_table():
                #exists table
                old_table = self.desc()
                if old_table != self.table:
                    if is_subset(old_table.nfields(), self.table.nfields()):
                        #upgrade table
                        self._upgrade_table()
                    else:
                        #replace table
                        self._replace_table
                else:
                    #table is the same as in database
                    pass
            else:
                #create new table
                self._create_table()

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
            create_sql = cursor.fetchall()[0][1]

            self.table = Table().fromsql(create_sql)

            logger.info("loading table %s...success.", self.name)
            return self
        except Exception, e:
            logger.info("loading table %s...failed. error: %s", self.name, str(e))
            raise e

    def desc(self):
        '''
               descrite table from storage
           :return:  Table
           '''
        try:
            sql = "show create table %s;" % self.name
            cursor = self.dbc.cursor()
            cursor.execute(sql)
            create_sql = cursor.fetchall()[0][1]

            table = Table().fromsql(create_sql)
            logger.info("describe table %s...success", self.name)

            return table
        except Exception, e:
            logger.error("describe table %s...failed. error %s", self.name, str(e))
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
           sql, models = "select %s from %s;" % (",".join(quotes(nfields, '`')), self.name), []
           cursor = self.dbc.cursor()
           cursor.execute(sql)
           results = cursor.fetchall()
           for result in results:
               model = {}
               for idx in range(0, len(result)):
                   nfield = nfields[idx]
                   vfield = result[idx]
                   if isinstance(vfield, str):
                       vfield = unescapes(vfield)
                   model[nfield] = vfield
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
            #get fields except default auto increment field
            nfields = []
            for field in self.table.fields:
                if not isinstance(field.default, AutoIncValue):
                    nfields.append(field.name)

            #prepare the values to be inserted
            values = []
            for model in models:
                value = []
                for nfield in nfields:
                    vfield = model.get(nfield)
                    if isinstance(vfield, str):
                        value.append(quotes(escapes(vfield)))
                    else:
                        value.append(objtostr(vfield))

                values.append("(%s)" % ",".join(value))

            sql = "insert into %s(%s) values %s;" % (self.name, ",".join(quotes(nfields, '`')), ",".join(values))
            self.dbc.cursor().execute(sql)
            self.dbc.commit()

            logger.info("insert into table %s...success", self.name)
        except Exception, e:
            logger.error("insert into table %s...failed. error %s", self.name, str(e))
            raise e

    def _create_table(self):
        '''
            create table in database
        :return:
        '''
        sql = self.table.tosql()
        self.dbc.cursor().execute(sql)

    def _replace_table(self):
        '''
            replace old table
        :return:
        '''
        from time import strftime

        #rename old table
        old_table_name = "%s_old_%s" % (self.name, strftime("%Y%m%d%H%M%S"))
        sql = "rename table %s to %s;" % (self.name, old_table_name)
        sql.dbc.cursor().execute(sql)

        #create new table
        self._create_table()

    def _upgrade_table(self):
        '''
            update table in database
        :return:
        '''
        after_column = None
        noldfields = self._table_fields()
        for field in self.table.fields:
            if not (field.name in noldfields):
                if after_column is not None:
                    sql = "alter table %s add column %s after %s" % (self.table.name, field.tosql(), after_column)
                else:
                    sql = "alter table %s add column %s;" % (self.table.name, field.tosql())
                self.dbc.cursor().execute(sql)
            after_column = field.name

    def _exists_table(self):
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

    def _table_fields(self):
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
