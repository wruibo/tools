'''
    operation for tables as interface
'''


class ITable:
    def __init__(self):
        self.name = None #table name
        self.table = None #table structure

    def create(self, *args):
        '''
            create table
        :return boolean, true for create success
        '''
        pass

    def load(self, *args):
        '''
            load table
        :return:  self or None
        '''
        pass

    def desc(self):
        '''
            descrite table from store
        :return:  Table
        '''
        pass

    def drop(self):
        '''
            drop table
        :return:
        '''
        pass

    def truncate(self):
        '''
            truncate table
        :return:
        '''

    def select(self):
        '''
            select all data from table
        :return:
        '''

    def insert(self, models):
        '''
            insert data to table
        :param models:
        :return:
        '''