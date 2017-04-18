from spider.storage.cindex import *
from spider.storage.ckey import *

from storage.cfield import *


class MetaTable(type):
    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)

    def __iter__(self):
        return self.select()

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass

    def __call__(self, *args, **kwargs):
        obj = type.__call__(self)
        obj.storage = args[0]

        return obj


class Table:
    __metaclass__ = MetaTable

    def create(self):
        pass

    def select(self, **where):
        print "select"

    def insert(self, item):
        print "insert"

    def update(self, item):
        print "update"

    def delete(self, **where):
        print "delete"


class LinkTable(Table):
    name = "tb_link"

    id = Field("id", Type.Int(), False, Value.AutoInc())
    url = Field("url", Type.String(512), False, None)
    ref = Field("ref", Type.String(512), True, None)
    fetched = Field("fetched", Type.Boolean(), True, None)
    fetch_time = Field("fetch_time", Type.BigInt(), True, None)

    k1 = Key.PrimaryKey("pk_id", "id")
    k2 = Key.NormalKey("normal_key", "id", "url")
    k3 = Key.UniqueKey("unique_key", "url", "ref")

    idx1 = Index.NormalIndex("normal_index", "id", "url")
    idx2 = Index.UniqueIndex("unique_index", "id", "url")


class MetaRecord(type):
    def __new__(cls, name, bases, attrs):
        if issubclass(cls, MetaRecord):
            table = attrs.get('__table__', None)

        return type.__new__(cls, name, (), attrs)

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass

    def __call__(self, *args, **kwargs):
        return type.__call__(self)

class Record:
    __metaclass__ = MetaRecord

    def __call__(self, *args, **kwargs):
        pass


class LinkRecord(Record):
    __table__ = LinkTable

if __name__ == '__main__':
    lt = LinkTable("abc", a=2)
    lt.insert(None)

    lr = LinkRecord()
    lr.url = "http://www.baidu.com"



    '''table = Table("tb_link", None)
    table.field("id", Type.Int(), False, Value.AutoInc())
    table.field("url", Type.String(512), False)
    table.field("ref", Type.String(512), True)
    table.field("fetched", Type.Boolean(), True)
    table.field("fetch_time", Type.BigInt(), True)

    table.key(Key.PrimaryKey, "pk_id", "id")

    table.key(Key.NormalKey, "normal_key", "id", "url")
    table.key(Key.UniqueKey, "unique_key", "url", "ref")

    table.index(Index.NormalIndex, "normal_index", "id", "url")
    table.index(Index.UniqueIndex, "unique_index", "id", "url")
    '''

    #print SQLHelper.sql_create_table(table)