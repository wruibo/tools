'''
    storage class
'''


class Storage:
    def __init__(self, name):
        self.name = name

    def create(self, table_schema):
        pass

    def drop(self, table_name):
        pass

    def truncate(self, table_name):
        pass

    def getall(self, table_name):
        pass

    def insert(self, table_name, records):
        pass
