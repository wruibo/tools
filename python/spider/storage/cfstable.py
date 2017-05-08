'''
    file system table
'''
import threading

from utility.cstr import *
from utility.cpath import *
from utility.clog import logger
from utility.clock import clock
from utility.cutil import is_subset

from storage.ctable import *
from storage.citable import *
from storage.cverifier import *

FSTableOperationError = Exception


class FSTable(ITable):
    '''
        table base on file
    '''
    def __init__(self):
        self.path = None
        self.table_file = None
        self.data_file = None

        self.lock = threading.Lock() #lock for operate table data

    def create(self, dbpath, table):
        '''
            create table
        :return self
        '''
        try:
            #initialize table parameters
            self.table = table
            self.name = table.name

            self.path = join_paths(dbpath, table.name)
            self.table_file = join_paths(self.path, "table")
            self.data_file = join_paths(self.path, "data")

            #create table directory if it is not exists
            make_dirs(self.path)

            #create or replace table file
            if is_file(self.table_file):

                #replace old table file if needed
                old_table = self.desc()
                if self.table != old_table:
                    if is_subset(old_table.nfields(), self.table.nfields()):
                        #upgrade data file
                        self._upgrade_data_file()
                    else:
                        #replace data file
                        self._replace_table_file()
                else:
                    #new table is same as exists table
                    pass
            else:
                #create new table file
                self._create_table_file()

            #create or upgrade or replace data file
            if is_file(self.data_file):
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.table.nfields() != nfields:
                        if is_subset(nfields, self.table.nfields()):
                            self._upgrade_data_file()
                        else:
                            self._replace_data_file()
            else:
                #create new data file
                self._create_data_file()

            logger.info("create table %s...success.", self.name)
            return self
        except Exception, e:
            logger.error("create table %s...failed. error: %s", self.name, str(e))
            raise e

    def load(self, dbpath, name):
        '''
            load table
        :return:  self
        '''
        try:
            #initialize table parameters
            self.name = name

            self.path = join_paths(dbpath, name)
            self.table_file = join_paths(self.path, "table")
            self.data_file = join_paths(self.path, "data")

            self.table = self.desc()

            #load data file
            if not is_file(self.data_file):
                #create data file if not exists
                self._create_data_file()
            else:
                #replace old data file if needed
                with open(self.data_file) as fdata:
                    nfields = strips(fdata.readline().split(","))
                    if self.table.nfields() != nfields:
                        if is_subset(nfields, self.table.nfields()):
                            self._upgrade_data_file()
                        else:
                            self._replace_data_file()

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
            with open(self.table_file) as ftable:
                table = Table().fromstr(ftable.read())
                return table
        except Exception, e:
            logger.info("describe table %s...failed. error: %s", self.name, str(e))
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
            raise e


    def truncate(self):
        '''
            truncate table
        :return:
        '''
        try:
            with clock(self.lock):
                remove_files(self.data_file)
                self._create_data_file()
        except Exception, e:
            logger.error("truncate table %s...failed. error %s", self.name, str(e))
            raise e


    def select(self):
        '''
            select all data from table
        :return:
        '''
        try:
            with clock(self.lock):
                with open(self.data_file, "r") as fdata:
                    models = []

                    #read field names
                    nfields = strips(fdata.readline().strip().split(","))
                    #read data records
                    data = fdata.readline()
                    while data:
                        data = data.strip()
                        vfields = strips(data.split(","))
                        model = {}
                        for idx in range(0, len(nfields)):
                            model[nfields[idx]] = str2obj(vfields[idx], ',')
                        models.append(model)
                        data = fdata.readline()

                    return models
        except Exception, e:
            logger.info("select data from table %s...failed. error: %s", self.name, str(e))
            raise e


    def insert(self, models):
        '''
            insert data to table
        :param models:
        :return:
        '''
        try:
            with clock(self.lock):
                with open(self.data_file, "a") as fdata:
                    lines = []
                    for model in models:
                        vfields = []
                        for nfield in self.table.nfields():
                            vfields.append(objtostr(model.get(nfield), ','))
                        lines.append("%s\n" % ",".join(vfields))
                    fdata.writelines(lines)
        except Exception, e:
            logger.info("insert data to table %s...failed. error: %s", self.name, str(e))
            raise e

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
            from time import strftime
            old_table_file = "%s.old.%s" % (self.table_file, strftime("%Y%m%d%H%M%S"))
            move(self.table_file, old_table_file)

        self._create_table_file()

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
            from time import strftime
            old_data_file = "%s.old.%s" % (self.data_file, strftime("%Y%m%d%H%M%S"))
            move(self.data_file, old_data_file)

        self._create_data_file()

    def _upgrade_data_file(self):
        '''
            upgrade data file to new table structure
        :return:
        '''
        #new fields for table
        newfields = self.table.fields

        #create new data file
        from time import strftime
        new_data_file = "%s.new.%s" % (self.data_file, strftime("%Y%m%d%H%M%S"))
        with open(new_data_file, 'w') as fnewdata:
            #write table header first
            fnewdata.write(",".join(self.table.nfields()) + "\n")

            #move old data to new data file
            with open(self.data_file) as folddata:
                #read old data file headers
                oldfields = {}
                noldfields = strips(folddata.readline().split(","))
                for i in range(0, len(noldfields)):
                    oldfields[noldfields[i]] = i

                #move old data to new data file
                old_data = folddata.readline()
                while old_data:
                    old_columns = strips(old_data.split(","))

                    new_columns = []
                    for i in range(0, len(newfields)):
                        idx = oldfields.get(newfields[i].name, None)
                        if idx:
                            #new column exists in old column
                            new_columns.append(objtostr(old_columns[idx], ","))
                        else:
                            #new column not exists in old column
                            new_columns.append(objtostr(newfields[i].default.value, ","))

                    fnewdata.write("%s\n".join(new_columns))

                    old_data = folddata.readline()

        #replace old data file with new data file
        old_data_file = "%s.old.%s" % (self.data_file, strftime("%Y%m%d%H%M%S"))
        move(self.data_file, old_data_file)
        move(new_data_file, self.data_file)

if __name__ == "__main__":
    pass
