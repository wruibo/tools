"""
    fund data from caifuqiao, site:
        http://beidou.aokebaer.com/
"""
import atl, dtl, dbm


class context:
    """
        context data for access caifuqiao
    """
    # access headers for caifuqiao
    _caifuqiao_access_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host": "beidou.aokebaer.com"
    }

    _caifuqiao_data_urls = {
        # net asset value url
        "nav": "http://beidou.aokebaer.com/api/fund_netvalue_list?fundId=%s&username=wangruibo@oak-inc.com&token=61b6e92659124055ce5d089cd6d364e7&role_id=2"
    }

    @staticmethod
    def headers():
        return context._caifuqiao_access_headers

    @staticmethod
    def url(url):
        return context._caifuqiao_data_urls.get(url)


class loader:
    """
        loader for fund data at caifuqiao
    """
    def __init__(self, code):
        self._code = code

    def nav(self):
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
        # fetch & parse the url data for fund @code
        url =  context.url("nav") % str(self._code)

        # get json data from url
        json_data = dbm.rqst.pgetjson(url, headers=context.headers())

        # extract results
        results = []

        # extract fund data from json content
        for record in json_data['data']['list']:
            results.append([dtl.xdate(record['value_date']), float(record['net_value']), float(record['total_value'])])
        return atl.matrix.reverser(results)

