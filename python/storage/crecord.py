from storage.cfield import *


class Record:
    def __init__(self):
        pass

class LinkTable(Table):
    name = "xxx"
    id = Field()
    index = Index()
    key = Key()

    def __init__(self, storage):
        pass

    def select(self):
        pass

class LinkRecord(Record):
    __table__ = LinkTable

    def select(self):
        pass

    def save(self):
        pass



if __name__ == "__main__":
    pass

