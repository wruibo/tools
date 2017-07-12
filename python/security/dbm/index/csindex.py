"""
    index from zhong zheng index, site:
        http://www.csindex.com.cn/
"""
import xml.dom
import xml.dom.minidom

import dtl
import requests
from dbm.index import loader
from dtl.core import xtype


class Context(loader.Context):
    """
        context data for access size china securities index
    """
    def __init__(self):
        # access headers for site china securities index
        self._csindex_access_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36"
        }

        # site china securities index data urls
        self._csindex_data_urls = {
            # index daily data url
            "day": "http://www.csindex.com.cn/sseportal/Day-K/%s.xml"
        }

    def headers(self):
        return self._csindex_access_headers

    def url(self, url):
        return self._csindex_data_urls.get(url)


class Loader(loader.Loader):
    """
        loader for get index data from site china securities index
    """
    def __init__(self):
        # initialize the loader's context
        loader.Loader.__init__(self, Context())

    def daily(self, code):
        """
            get daily index data from csindex
        :param code: index code at csindex
        :return: list of price list, [['date', 'open', 'close', 'high', 'low', 'volume', 'amount'], ...]
        """
        # fetch data from daily index data url
        url = self.url("day") % (code)
        content = requests.get(url, headers=self.headers()).text
        dom = xml.dom.minidom.parseString(content)

        # parse index daily records
        pricetbl = dtl.table([['date', 'open', 'close', 'high', 'low', 'volume', 'amount']])
        elmts = dom.getElementsByTagName("smbol")
        for elmt in elmts:
            # parse each record
            date = elmt.getAttribute("tdd") if elmt.hasAttribute("tdd") else None
            open = float(elmt.getAttribute("op")) if elmt.hasAttribute("op") else None
            close = float(elmt.getAttribute("ep")) if elmt.hasAttribute("ep") else None
            high = float(elmt.getAttribute("hp")) if elmt.hasAttribute("hp") else None
            low = float(elmt.getAttribute("lp")) if elmt.hasAttribute("lp") else None
            volume = float(elmt.getAttribute("vol")) if elmt.hasAttribute("vol") else None
            amount = float(elmt.getAttribute("tot")) if elmt.hasAttribute("tot") else None

            # add to prices list
            pricetbl.addrow([date, open, close, high, low, volume, amount])

        return pricetbl
