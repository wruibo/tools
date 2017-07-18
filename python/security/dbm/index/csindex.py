"""
    index from zhong zheng index, site:
        http://www.csindex.com.cn/
"""
import xml.dom
import xml.dom.minidom

import dtl, utl, dbm
import requests


class context:
    """
        context data for access size china securities index
    """
    # access headers for site china securities index
    _csindex_access_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36"
    }

    # site china securities index data urls
    _csindex_data_urls = {
        # index daily data url
        "price-daily": "http://www.csindex.com.cn/sseportal/Day-K/%s.xml"
    }

    @staticmethod
    def headers():
        return context._csindex_access_headers

    @staticmethod
    def url(url):
        return context._csindex_data_urls.get(url)


class loader:
    """
        loader for get index data from site china securities index
    """
    def __init__(self, code):
        self.price = loader.price(code)

    class price:
        """
            load price from source site
        """
        def __init__(self, code):
            self._code = code

        def daily(self):
            """
                get daily index data from csindex, data format:
                [
                    [date, open, close, high, low, volume, amount],
                    [...]
                ]
            :param code: index code at csindex
            :return: list of price list
            """
            # fetch data from daily index data url
            url = context.url("price-daily") % (self._code)

            content, needcache = dbm.cache.take(utl.hash.sha1(url.encode())), False
            if content is None:
                content = requests.get(url, headers=context.headers()).text
                needcache = True

            # parse content
            dom = xml.dom.minidom.parseString(content)

            # cache data
            if needcache:
                dbm.cache.save(utl.hash.sha1(url.encode()), content)

            # parse index daily records
            prices = []
            elmts = dom.getElementsByTagName("smbol")
            for elmt in elmts:
                # parse each record
                date = dtl.xday(elmt.getAttribute("tdd"), "%Y%m%d") if elmt.hasAttribute("tdd") else None
                open = float(elmt.getAttribute("op")) if elmt.hasAttribute("op") else None
                close = float(elmt.getAttribute("ep")) if elmt.hasAttribute("ep") else None
                high = float(elmt.getAttribute("hp")) if elmt.hasAttribute("hp") else None
                low = float(elmt.getAttribute("lp")) if elmt.hasAttribute("lp") else None
                volume = float(elmt.getAttribute("vol")) if elmt.hasAttribute("vol") else None
                amount = float(elmt.getAttribute("tot")) if elmt.hasAttribute("tot") else None

                # add to prices list
                prices.append([date, open, close, high, low, volume, amount])

            return prices
