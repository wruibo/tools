from storage.cmodel import *
from storage.ctable import *
from storage.cdbstorage import *
from storage.cfsstorage import *


class DemoTable(Table):
    '''
        demo table
    '''
    name = "tb_demo"

    id = Field("id", Int(), AutoIncValue())
    code = Field("code", Int(), StringValue(32), NotNullValue())

    pk = PrimaryKey(id, code)

    def __init__(self, name="tb_demo"):
        Table.__init__(self, name)

        self.field("id", Int(), AutoIncValue())
        self.field("code", String(32), NotNullValue())
        self.field("name", String(32), StringValue("abc"))
        self.field("valid", Boolean(), BooleanValue(False))
        self.field("create_time", BigInt())

        self.key(PrimaryKey, "pk_id", "id")
        self.key(NormalKey, "normal_key", "name", "code")
        self.key(UniqueKey, "unique_key", "code", "valid")


class DemoModel(Model):
    table = DemoTable()

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.name = kwargs.get("name", None)
        self.valid = kwargs.get("valid", False)
        self.create_time = kwargs.get("create_time", 0)

    def randoms(self, num):
        import time

        models = []
        for i in range(1, num+1):
            models.append(DemoModel(code="code%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return models


class UpgradeDemoTable(Table):
    def __init__(self, name="tb_demo"):
        Table.__init__(self, name)

        self.field("id", Int(), AutoIncValue())
        self.field("code", String(32), NotNullValue())
        self.field("name", String(32), StringValue("abc"))
        self.field("age", Int(), NumberValue(0))
        self.field("desc", Text(), DefaultNullValue())
        self.field("valid", Boolean(), BooleanValue(False))
        self.field("create_time", BigInt())
        self.field("update_time", BigInt(), NumberValue(0))

        self.key(PrimaryKey, "pk_id", "id")
        self.key(NormalKey, "desc_key", "desc")
        self.key(NormalKey, "normal_key", "name", "code")
        self.key(UniqueKey, "unique_key", "code", "valid")


class UpgradeDemoModel(Model):
    table = UpgradeDemoTable()

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.name = kwargs.get("name", None)
        self.age = kwargs.get("age", 0)
        self.desc = kwargs.get("desc", "desc")
        self.valid = kwargs.get("valid", False)
        self.create_time = kwargs.get("create_time", 0)
        self.update_time = kwargs.get("update_time", 0)

    def randoms(self, num):
        import time

        models = []
        for i in range(1, num+1):
            models.append(UpgradeDemoModel(code="code1%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return models

class TestModel(Model):
    table = DemoTable

if __name__ == "__main__":
    model = TestModel()

    #create storage first
    dbstorage = DBStorage().open("localhost", "root", "root", "db_demo")
    fsstorage = FSStorage().open("./storage/db_demo")

    #clear exist database first
    dbstorage.drop_tables()
    fsstorage.drop_tables()

    #create demo table
    table1 = DemoTable()

    #create table1 first
    dbstorage.create_table(table1)
    fsstorage.create_table(table1)

    #insert data to table1
    dbstorage.insert_into_table(table1.name, DemoModel().randoms(5))
    fsstorage.insert_into_table(table1.name, DemoModel().randoms(5))

    #get data from tabl1
    dbstorage.select_from_table(table1.name)
    fsstorage.select_from_table(table1.name)

    #create upgrade demo table
    table2 = UpgradeDemoTable()

    #upgrade table1 to table2
    dbstorage.create_table(table2)
    fsstorage.create_table(table2)

    #insert data to upgrade table
    dbstorage.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))
    fsstorage.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))

    #get data from upgrade table
    dbstorage.select_from_table(table2.name)
    fsstorage.select_from_table(table2.name)


