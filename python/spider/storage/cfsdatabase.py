'''
    file system based database
'''
import threading

from utility.clog import logger

from utility.cdir import cdir
from utility.cpath import cpath
from utility.clock import clock

from storage.cfstable import FStable
from storage.cfsschema import FSSchema


class FSDatabase:
    def __init__(self, path):
        self.path = path
        self.table_path = cpath.join(path, "table")
        self.schema_path = cpath.join(path, "schema")

        self.tables = [] #file system tables

        self.lock = threading.Lock() #database lock

    @staticmethod
    def create(path):
        '''
            create database if not exist, or load database
        :return:
        '''
        database = FSDatabase(path)
        database.create_database()

        return database, None

    def create_database(self):
        '''
            create database if not exist, or load database
        :return:
        '''
        with clock(self.lock):
            # create database
            self._create()

            # load database
            self._load()

    def create_table(self, schema):
        '''
            create table in current database
        :param table:
        :return:
        '''
        with clock(self.lock):
            # test if the table of schema has loaded
            if self._table_loaded(schema):
                logger.info("create table %s...exists.", schema.name)
                return

            #save schema to schema file
            error = FSSchema.save(cpath.join(self.schema_path, schema.name), schema)
            if error is not None:
                logger.error("create table %s...failed. error: %", schema.name, error)
                return


            #create table with schema
            table, error = FStable.create(cpath.join(self.table_path, schema.name), schema)
            if table is not None:
                self.tables.append(table)
                logger.info("create table %s...success.", schema.name)
            else:
                logger.error("create table %s...failed. error: ", schema.name, error)

    def drop_table(self, table_name):
        '''
            drop table in current database
        :param table_name:
        :return:
        '''
        with clock(self.lock):
            for table in self.tables:
                if table.name==table_name:
                    table.drop()
                    self.tables.remove(table)


    def truncate_table(self, table_name):
        '''
            truncate table data
        :param table_name:
        :return:
        '''
        with clock(self.lock):
            for table in self.tables:
                if table.name==table_name:
                    table.truncate()

    def select_from_table(self, table_name):
        '''
            select all records from table
        :param table_name:
        :param recordcls:
        :return:
        '''
        with clock(self.lock):
            for table in self.tables:
                if table.name==table_name:
                    return table.select()

    def insert_into_table(self, table_name, records):
        '''
            insert records into table
        :param table_name:
        :param records:
        :return:
        '''
        with clock(self.lock):
            for table in self.tables:
                if table.name == table_name:
                    table.insert(records)


    def _create(self):
        '''
            create database directory if not exists
        :return:
        '''
        #create database's root directory
        if not cpath.exists(self.path):
            cdir.makes(self.path)

        #create table's directory
        if not cpath.exists(self.table_path):
            cdir.makes(self.table_path)

        #create table schema's directory
        if not cpath.exists(self.schema_path):
            cdir.makes(self.schema_path)

    def _load(self):
        '''
            load table schemas and tables
        :return:
        '''
        #load table schemas first
        schemas = {}
        schema_files = cdir.files(self.schema_path)
        for schema_file in schema_files:
                schema, error = FSSchema.load(schema_file)
                if schema is not None:
                    schemas[schema.name] = schema
                    logger.info("load schema from file %s... success.")
                else:
                    logger.warning("load schema from file %s... failed, error: %s", schema_file, error)

        #then load tables related with table schemas
        table_files = cdir.files(self.table_path)
        for table_file in table_files:
            schema = schemas.get(table_file)
            if schema is not None:
                table, error = FStable.load(cpath.join(self.table_path, table_file), schema)
                if table is not None:
                    self.tables.append(table)
                    logger.info("load table from file %s... success.", table_file)
                else:
                    logger.warning("load table from file %s... failed. error: %s", table_file, error)
            else:
                logger.warning("load table from file %s... failed. error: no relate table schema.", table_file)

    def _table_loaded(self, schema):
        '''
            test if table(schema) has loaded
        :param table:
        :return:
        '''
        for table in self.tables:
            if table.match(schema):
                return True

        return False

