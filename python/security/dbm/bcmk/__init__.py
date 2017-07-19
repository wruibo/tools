"""
    benchmark for portfolio return&risk analysis
"""
import dbm

hushen300 = dbm.index.price("000300")
shangzhengzz = dbm.index.price("000001")
shangzheng50 = dbm.index.price("000016")
zhongzheng100 = dbm.index.price("000903")
zhongzheng200 = dbm.index.price("000904")
zhongzheng500 = dbm.index.price("000905")
zhongzheng700 = dbm.index.price("000907")


if __name__ == "__main__":
    print(hushen300.daily())