'''
    file system table
'''

from utility.cstr import *
from utility.cpath import *
from utility.clog import logger


from storage.ckey import *
from storage.ctype import *
from storage.cindex import *
from storage.cvalue import *
from storage.cfield import *
from storage.cverifier import *
from storage.cschema import Schema

FSTableOperationError = Exception


class FStable:
    '''
        table base on file
    '''
    def __init__(self, dbpath, name, schema=None):
        self.path = join_paths(dbpath, name)
        self.name = name
        self.schema = schema

        self.schema_file = join_paths(self.path, "schema")
        self.data_file = join_paths(self.path, "data")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load(self):
        '''
            load table
        :return:  self or None
        '''
        try:
            #schema file must be exist
            if not is_file(self.schema_file):
                raise FSTableOperationError("schema file not exist.")

            #load schema file
            with open(self.schema_file, 'r') as fschema:
                self.schema = Schema().fromstr(fschema.read())

            #load data file
            if not is_file(self.data_file):
                #create data file if not exists
                self._create_data_file()
            else:
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.schema.nfields() != nfields:
                        self._replace_data_file()

            logger.info("loading table %s...success.", self.name)
            return self
        except Exception, e:
            logger.info("loading table %s...failed. error: %s", self.name, e.message)

    def create(self):
        '''
            create table
        :return boolean, true for create success
        '''
        if self.schema is None:
            return False

        try:
            make_dirs(self.path)

            #create schema file
            if is_file(self.schema_file):
                #replace old schema file if needed
                with open(self.schema_file) as fschema:
                    try:
                        schema = Schema().fromstr(fschema.read())
                        if self.schema != schema:
                            self._replace_schema_file()
                    except:
                        self._replace_schema_file()
            else:
                #create new schema file
                self._create_schema_file()

            #create data file
            if is_file(self.data_file):
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.schema.nfields() != nfields:
                        self._replace_data_file()
            else:
                #create new data file
                self._create_data_file()

            logger.info("create table %s...success.", self.name)
            return True
        except Exception, e:
            logger.error("create table %s...failed. error: %s", self.name, str(e))
            return False

    def drop(self):
        '''
            drop table
        :return:
        '''
        try:
            remove_dir(self.path)
        except Exception, e:
            logger.error("drop table %s...failed. error %s", self.name, str(e))


    def truncate(self):
        '''
            truncate table
        :return:
        '''
        try:
            remove_files(self.data_file)
            self._create_data_file()
        except Exception, e:
            logger.error("truncate table %s...failed. error %s", self.name, str(e))

    def getall(self):
        '''
            get all records from table
        :return:
        '''


    def insert(self, records):
        '''
            insert records to table
        :param records:
        :return:
        '''
        pass

    def _create_schema_file(self):
        '''
            create schema file
        :return:
        '''
        with open(self.schema_file, 'w') as fschema:
            fschema.write(self.schema.tostr())

    def _replace_schema_file(self):
        '''
            replace schema file
        :return:
        '''
        if is_file(self.schema_file):
            import time
            old_schema_file = "%s.old.%s" % (self.schema_file, str(time.time()))
            move(self.schema_file, old_schema_file)
            self._create_schema_file()
        else:
            raise FSTableOperationError("replace schema file failed. error: %s is not file.", self.schema_file)


    def _create_data_file(self):
        '''
            create data file
        :return:
        '''
        with open(self.data_file, 'w') as fdata:
            fdata.write(",".join(self.schema.nfields()) + "\n")

    def _replace_data_file(self):
        '''
            replace data file
        :return:
        '''
        if is_file(self.data_file):
            import time
            old_data_file = "%s.old.%s" %(self.data_file, str(time.time()))
            move(self.data_file, old_data_file)
            self._create_data_file()
        else:
            raise FSTableOperationError("replace data file failed. error: %s is not file.", self.data_file)


if __name__ == "__main__":
    schema = Schema("tb_demo")
    schema.field("id", Int(), False, AutoIncValue())
    schema.field("code", String(32), False)
    schema.field("name", String(32), True)
    schema.field("valid", Boolean(), True)
    schema.field("create_time", BigInt(), True)

    schema.key(PrimaryKey, "pk_id", "id")
    schema.key(NormalKey, "normal_key", "name","code")
    schema.key(UniqueKey, "unique_key", "code", "valid")

    schema.index(NormalIndex, "normal_index", "name", "code")
    schema.index(UniqueIndex, "unique_index", "code", "valid")

    table = FStable("./", schema.name, schema)
    table.create()

    table1 = FStable("./", "tb_demo").load()
    table1.truncate()
