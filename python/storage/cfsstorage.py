'''
    file system storage
'''
from storage import Storage


class FSStorage(Storage):
    def __init__(self, path):
        Storage.__init__(self)
        self.path = path

    def create(self, table):
        pass

