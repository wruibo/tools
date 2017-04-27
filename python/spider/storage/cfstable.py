'''
    file system table
'''
from utility.cpath import *
from utility.clog import logger
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
            load table @name from database
        :param dbpath:
        :param name:
        :return:
        '''
        try:
            with open(self.schema_file, 'r') as fschema:
                self.schema = Schema.fromstr(fschema.read())
                self.check()
                logger.info("loading table %s...success.", self.name)
                return True
        except Exception, e:
            logger.info("loading table %s...failed. error: %s", self.name, e.message)

    def create(self):
        '''
            create table with @schema
        :param dbpath:
        :param schema:
        :return:
        '''
        if self.schema is None:
            return False

        try:
            make_dirs(self.path)

            #create schema file
            if is_file(self.schema_file):
                #replace old schema file if needed
                with open(self.schema_file) as fschema:
                    schema = Schema.fromstr(fschema.read())
                    if self.schema != schema:
                        self._replace_schema_file()
                    else:
                        pass
            else:
                #create new schema file
                self._create_schema_file()

            #create data file
            if is_file(self.data_file):
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    from utility.cstr import *
                    nfields = strips(fdata.readline().split(","))
                    if self.schema.nfields() != nfields:
                        self._replace_data_file()
                    else:
                        pass
            else:
                #create new data file
                self._create_data_file()

            logger.info("creating table %s...success.", self.name)
            return True
        except Exception, e:
            logger.error("creating table %s...failed. error: %s", self.name, str(e))
            return False

    def drop(self):
        pass

    def truncate(self):
        pass

    def match(self, schema):
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
    from storage.ctype import Type
    from storage.ckey import Key
    from storage.cindex import Index
    from storage.cvalue import Value

    schema = Schema("tb_demo")
    schema.field("id", Type.Int(), False, Value.AutoInc())
    schema.field("code", Type.String(32), False)
    schema.field("name", Type.String(32), True)
    schema.field("valid", Type.Boolean(), True)
    schema.field("create_time", Type.BigInt(), True)

    schema.key(Key.PrimaryKey, "pk_id", "id")
    schema.key(Key.NormalKey, "normal_key", "name","code")
    schema.key(Key.UniqueKey, "unique_key", "code", "valid")

    schema.index(Index.NormalIndex, "normal_index", "name", "code")
    schema.index(Index.UniqueIndex, "unique_index", "code", "valid")

    table = FStable("./", schema.name, schema)
    table.create()