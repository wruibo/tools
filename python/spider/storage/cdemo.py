from storage.cmodel import *
from storage.ctable import *
from storage.cdbstorage import *
from storage.cfsstorage import *


class DemoTable(Table):
    f1 = Field("id", Int(), AutoIncValue())
    f2 = Field("code", String(32), NotNullValue())
    f3 = Field("name", String(32), StringValue("abc"))
    f4 = Field("valid", Boolean(), BooleanValue(False))
    f5 = Field("create_time", BigInt())

    k1 = PrimaryKey("pk_id", "id")
    k2 = NormalKey("normal_key", "name", "code")
    k3 = UniqueKey("unique_key", "code", "valid")


class DemoModel(Model):
    table = DemoTable("tb_demo")

    def randoms(self, num):
        import time

        models = []
        for i in range(1, num+1):
            models.append(DemoModel(code="code%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return models


class UpgradeDemoTable(Table):
    f1 = Field("id", Int(), AutoIncValue())
    f2 = Field("code", String(32), NotNullValue())
    f3 = Field("name", String(32), StringValue("abc"))
    f4 = Field("age", Int(), NumberValue(0))
    f5 = Field("desc", Text(), DefaultNullValue())
    f6 = Field("valid", Boolean(), BooleanValue(False))
    f7 = Field("create_time", BigInt())

    k1 = PrimaryKey("pk_id", "id")
    k2 = NormalKey("valid_key", "valid")
    k3 = NormalKey("normal_key", "name", "code")
    k4 = UniqueKey("unique_key", "code", "valid")


class UpgradeDemoModel(Model):
    table = UpgradeDemoTable("tb_demo")

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
    table1 = DemoTable("tb_demo")

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
    table2 = UpgradeDemoTable("tb_demo")

    #upgrade table1 to table2
    dbstorage.create_table(table2)
    fsstorage.create_table(table2)

    #insert data to upgrade table
    dbstorage.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))
    fsstorage.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))

    #get data from upgrade table
    dbstorage.select_from_table(table2.name)
    fsstorage.select_from_table(table2.name)


