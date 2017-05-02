'''
    storage class
'''


class Storage:
    def __init__(self):
        pass

    def open(self, *args, **kwargs):
        '''
            open storage
        :param args:
        :param kwargs:
        :return: (storage, error)
        '''
        pass

    def close(self):
        pass

    def create_table(self, table):
        '''
            create table in storage
        :param table:
        :return:
        '''
        pass

    def drop_table(self, table):
        '''
            drop table in storage
        :param table:
        :return:
        '''
        pass

    def truncate_table(self, table):
        '''
            truncate table in storage
        :param table:
        :return:
        '''
        pass

    def select_from_table(self, table):
        '''
            select data from table in storage
        :param table:
        :return:
        '''
        pass

    def insert_into_table(self, table, models):
        '''
            insert data into table in storage
        :param table:
        :param models:
        :return:
        '''
        pass
