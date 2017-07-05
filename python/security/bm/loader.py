'''
    loader for stock index benchmark
'''
from bm.index import Price, Index

import requests
import xml.dom.minidom


class _Loader:
    def __init__(self):
        pass

    def load(self, code):
        pass


class _LoaderZZ(_Loader):
    def __init__(self, url):
        self.url = url

    def load(self):
        dom = xml.dom.minidom.parseString(requests.get(self.url).text)

        # parse index code and name
        elmts = dom.getElementsByTagName("data")
        index = Index(elmts[0].getAttribute("ZSDM"), elmts[0].getAttribute("ZSMC"), elmts[0].getAttribute("EN"))

        # parse price records
        elmts = dom.getElementsByTagName("smbol")
        for elmt in elmts:
            price = Price()

            price.time = elmt.getAttribute("tdd") if elmt.hasAttribute("tdd") else None
            price.open = float(elmt.getAttribute("op")) if elmt.hasAttribute("op") else None
            price.close = float(elmt.getAttribute("ep")) if elmt.hasAttribute("ep") else None
            price.high = float(elmt.getAttribute("hp")) if elmt.hasAttribute("hp") else None
            price.low = float(elmt.getAttribute("lp")) if elmt.hasAttribute("lp") else None
            price.volume = float(elmt.getAttribute("vol")) if elmt.hasAttribute("vol") else None
            price.amount = float(elmt.getAttribute("tot")) if elmt.hasAttribute("tot") else None

            index.prices.append(price)

        return index

_loaders = {
    "shzz": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000001.xml"),
    "sz50": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000016.xml"),
    "hs300": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000300.xml"),
    "zz100": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000903.xml"),
    "zz200": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000904.xml"),
    "zz500": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000905.xml"),
    "zz700": _LoaderZZ("http://www.csindex.com.cn/sseportal/Day-K/000907.xml")
}


def load(code):
    loader = _loaders.get(code.lower(), None)
    return None if loader is None else loader.load()
