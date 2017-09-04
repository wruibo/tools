"""
    benchmark for portfolio return&risk analysis
"""
from .. import index as _index

hushen300 = _index.price("000300")
shangzhengzz = _index.price("000001")
shangzheng50 = _index.price("000016")
zhongzheng100 = _index.price("000903")
zhongzheng200 = _index.price("000904")
zhongzheng500 = _index.price("000905")
zhongzheng700 = _index.price("000907")


if __name__ == "__main__":
    print(hushen300.daily())