from storage.cmodel import *
from storage.ctable import *
from storage.cdbstorage import *
from storage.cfsstorage import *


class DemoTable(Table):
    id = Field("id", Int(), AutoIncValue())
    code = Field("code", String(32), NotNullValue())
    name = Field("name", String(32), StringValue("abc"))
    valid = Field("valid", Boolean(), BooleanValue(False))
    create_time = Field("create_time", BigInt())

    pk_id = PrimaryKey("pk_id", "id")
    normal_key = NormalKey("normal_key", "name", "code")
    unique_key = UniqueKey("unique_key", "code", "valid")


class DemoModel(Model):
    table = DemoTable()

    def randoms(self, num):
        import time

        models = []
        for i in range(1, num+1):
            models.append(DemoModel(code="code%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return models


class UpgradeDemoTable(Table):
    id = Field("id", Int(), AutoIncValue())
    code = Field("code", String(32), NotNullValue())
    name = Field("name", String(32), StringValue("abc"))
    age = Field("age", Int(), NumberValue(0))
    desc = Field("desc", Text(), DefaultNullValue())
    valid = Field("valid", Boolean(), BooleanValue(False))
    create_time = Field("create_time", BigInt())

    pk_id = PrimaryKey("pk_id", "id")
    valid_key = NormalKey("valid_key", "valid")
    normal_key = NormalKey("normal_key", "name", "code")
    unique_key = UniqueKey("unique_key", "code", "valid")


class UpgradeDemoModel(Model):
    table = UpgradeDemoTable()

    def randoms(self, num):
        import time

        models = []
        for i in range(1, num+1):
            models.append(UpgradeDemoModel(code="code1%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return models

if __name__ == "__main__":
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


