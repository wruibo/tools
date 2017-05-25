from util.timer import *
from store.table import *
from store.dbstore import *
from store.fsstore import *

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
    #create store first
    dbstore = DBStore().open("localhost", "root", "root", "db_demo")
    fsstore = FSStore().open("./store/db_demo")

    #clear exist database first
    dbstore.drop_tables()
    fsstore.drop_tables()

    #create demo table
    table1 = DemoTable("tb_demo")

    #create table1 first
    dbstore.create_table(table1)
    fsstore.create_table(table1)

    #insert data to table1
    dbstore.insert_into_table(table1.name, DemoModel().randoms(5))
    fsstore.insert_into_table(table1.name, DemoModel().randoms(5))

    #get data from tabl1
    dbstore.select_from_table(table1.name)
    fsstore.select_from_table(table1.name)

    #create upgrade demo table
    table2 = UpgradeDemoTable("tb_demo")

    #upgrade table1 to table2
    dbstore.create_table(table2)
    fsstore.create_table(table2)

    #insert data to upgrade table
    dbstore.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))
    fsstore.insert_into_table(table2.name, UpgradeDemoModel().randoms(5))

    #get data from upgrade table
    dbstore.select_from_table(table2.name)
    fsstore.select_from_table(table2.name)


