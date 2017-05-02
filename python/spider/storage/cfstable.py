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
from storage.ctable import *
from storage.cverifier import *

FSTableOperationError = Exception


class FSTable:
    '''
        table base on file
    '''
    def __init__(self):
        self.path = None
        self.name = None
        self.table_file = None
        self.data_file = None

        self.table = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load(self, dbpath, name):
        '''
            load table
        :return:  self or None
        '''
        try:
            #initialize table parameters
            self.path = join_paths(dbpath, name)
            self.name = name
            self.table_file = join_paths(self.path, "table")
            self.data_file = join_paths(self.path, "data")

            #table file must be exist
            if not is_file(self.table_file):
                raise FSTableOperationError("table file not exist.")

            #load table file
            with open(self.table_file, 'r') as ftable:
                self.table = Table().fromstr(ftable.read())

            #load data file
            if not is_file(self.data_file):
                #create data file if not exists
                self._create_data_file()
            else:
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.table.nfields() != nfields:
                        self._replace_data_file()

            logger.info("loading table %s...success.", self.name)
            return self
        except Exception, e:
            logger.info("loading table %s...failed. error: %s", self.name, str(e))
            raise e

    def create(self, dbpath, table):
        '''
            create table
        :return boolean, true for create success
        '''
        try:
            #initialize table parameters
            self.path = join_paths(dbpath, table.name)
            self.name = table.name
            self.table_file = join_paths(self.path, "table")
            self.data_file = join_paths(self.path, "data")
            self.table = table

            #create table directory
            make_dirs(self.path)

            #create table file
            if is_file(self.table_file):
                #replace old table file if needed
                with open(self.table_file) as ftable:
                    try:
                        table = Table().fromstr(ftable.read())
                        if self.table != table:
                            self._replace_table_file()
                    except:
                        self._replace_table_file()
            else:
                #create new table file
                self._create_table_file()

            #create data file
            if is_file(self.data_file):
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.table.nfields() != nfields:
                        self._replace_data_file()
            else:
                #create new data file
                self._create_data_file()

            logger.info("create table %s...success.", self.name)
            return self
        except Exception, e:
            logger.error("create table %s...failed. error: %s", self.name, str(e))
            raise e

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

    def select(self):
        '''
            select all data from table
        :return:
        '''
        with open(self.data_file, "r") as fdata:
            models = []

            #read field names
            nfields = fdata.readline().strip().split(",")
            #read data records
            data = fdata.readline()
            while data:
                data = data.strip()
                vfields = data.split(",")
                model = {}
                for idx in range(0, len(nfields)):
                    model[nfields[idx]] = str2obj(vfields[idx])
                models.append(model)
                data = fdata.readline()

            return models


    def insert(self, models):
        '''
            insert data to table
        :param models:
        :return:
        '''
        with open(self.data_file, "a") as fdata:
            lines = []
            for model in models:
                vfields = []
                for nfield in self.table.nfields():
                    vfields.append(objtostr(model.get(nfield)))
                lines.append("%s\n"%",".join(vfields))
            fdata.writelines(lines)

    def _create_table_file(self):
        '''
            create table file
        :return:
        '''
        with open(self.table_file, 'w') as ftable:
            ftable.write(self.table.tostr())

    def _replace_table_file(self):
        '''
            replace table file
        :return:
        '''
        if is_file(self.table_file):
            import time
            old_table_file = "%s.old.%s" % (self.table_file, str(time.time()))
            move(self.table_file, old_table_file)
            self._create_table_file()
        else:
            raise FSTableOperationError("replace table file failed. error: %s is not file.", self.table_file)


    def _create_data_file(self):
        '''
            create data file
        :return:
        '''
        with open(self.data_file, 'w') as fdata:
            fdata.write(",".join(self.table.nfields()) + "\n")

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
    table = Table("tb_demo")
    table.field("id", Int(), False, AutoIncValue())
    table.field("code", String(32), False)
    table.field("name", String(32), True)
    table.field("valid", Boolean(), True)
    table.field("create_time", BigInt(), True)

    table.key(PrimaryKey, "pk_id", "id")
    table.key(NormalKey, "normal_key", "name","code")
    table.key(UniqueKey, "unique_key", "code", "valid")

    table.index(NormalIndex, "normal_index", "name", "code")
    table.index(UniqueIndex, "unique_index", "code", "valid")

    ftable = FSTable()
    ftable.create("./", table)

    from storage.cmodel import DemoModel
    ftable.insert(DemoModel().randoms(10))

    ftable1 = FSTable().load("./", table.name)
    print ftable1.select()