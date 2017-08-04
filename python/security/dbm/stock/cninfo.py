"""
    stock data from cninfo, web site:
    http://www.cninfo.com.cn/
"""
import atl, dtl, dbm, requests


class context:
    """
        context data for access caifuqiao
    """
    # access headers for caifuqiao
    _cninfo_access_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host": "www.cninfo.com.cn"
    }

    _cninfo_data_urls = {
        # net asset value url
        "finance": "http://www.cninfo.com.cn/cninfo-new/data/download",
        "quotation": "http://www.cninfo.com.cn/cninfo-new/data/download"
    }

    @staticmethod
    def headers():
        return context._cninfo_access_headers

    @staticmethod
    def url(url):
        return context._cninfo_data_urls.get(url)


class loader:
    """
        loader for fund data at caifuqiao
    """
    def __init__(self, market, code):
        self._market = market
        self._code = code

    def finance(self, start_year, end_year):
        """
            load fund nav from caifuqiao by its code in caifuqiao.
        data format:
            [
                [date, nav, aav],
                [...]
            ]
        :param code: str, fund code in caifuqiao
        :return: matrix, nav records
        """
        # post form data
        form_data = {
            "market": self._market,
            "type": "fzb",
            "code": self._code,
            "minYear": str(start_year),
            "maxYear": str(end_year)
        }

        # fetch & parse the url data for fund @code
        url =  context.url("finance")

        # get json data from url
        req = requests.post(url, form_data, headers=context.headers())

        with open("./tt.zip", 'wb') as f:
            f.write(req.content)


    def quotation(self, start_year, end_year):
        """
            load fund nav from caifuqiao by its code in caifuqiao.
        data format:
            [
                [date, nav, aav],
                [...]
            ]
        :param code: str, fund code in caifuqiao
        :return: matrix, nav records
        """
        # post form data
        form_data = {
            "market": self._market,
            "type": "hq",
            "code": self._code,
            "minYear": str(start_year),
            "maxYear": str(end_year)
        }

        # fetch & parse the url data for fund @code
        url =  context.url("finance")

        # get json data from url
        req = requests.post(url, form_data, headers=context.headers())

        with open("./tt.zip", 'wb') as f:
            f.write(req.content)


if __name__ == "__main__":
    ld = loader('sz', '000001')
    ld.finance(2015, 2017)
