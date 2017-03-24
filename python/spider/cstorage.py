'''
    storage for storing content
'''


class Storage:
    def __init__(self):
        pass

    def store(self, storable):
        pass


class MysqlStorage(Storage):
    def store(self, storable):
        pass


class JsonFileStorage(Storage):

    def store(self, name, data):
        pass


class StorageMgr(Storage):

    def load(self, storage):
        pass

    def store(self, name, data):
        pass