'''
    base store class
'''


class IStore:
    def __init__(self):
        self.tindexs = {} # table index by name
        self.tables = []  # tables in store

    def open(self, *args, **kwargs):
        '''
            open store
        :param args:
        :param kwargs:
        :return: (store, error)
        '''
        pass

    def close(self):
        '''
            close store
        :return:
        '''
        pass

    def create_table(self, table):
        '''
            create table in store
        :param table:
        :return:
        '''
        pass

    def describe_tables(self):
        '''
            describe all table structures
        :return:
        '''
        pass

    def drop_table(self, name):
        '''
            drop table in store
        :param name:
        :return:
        '''
        pass

    def drop_tables(self):
        '''
            clear all tables in store
        :return:
        '''
        pass

    def truncate_table(self, name):
        '''
            truncate table data
        :param name:
        :return:
        '''
        table = self.tables[self.tindexs[name]]
        table.truncate()

    def select_from_table(self, name):
        '''
            select all records from table
        :param name:
        :return:
        '''
        table = self.tables[self.tindexs[name]]
        return table.select()

    def insert_into_table(self, name, models):
        '''
            insert records into table
        :param name:
        :param models:
        :return:
        '''
        table = self.tables[self.tindexs[name]]
        table.insert(models)

    def _rebuild_tindex(self):
        '''
            rebuild table index->pos
        :return:
        '''
        self.tindexs = {}
        for idx in range(0, len(self.tables)):
            self.tindexs[self.tables[idx].table.name] = idx
