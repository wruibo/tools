"""
    fund data from simuwang, site:
        http://www.simuwang.com/
"""
import dtl
import json
import requests
from dbm.fund import loader
from dtl.core import xtype
from util import xmatrix


class Context(loader.Context):
    """
        context data for access simuwang
    """
    def __init__(self):
        # access headers for simuwang
        self._simuwang_access_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
            "Host": "dc.simuwang.com",
            "Cookie": "regsms=1489648164000; guest_id=1489648267; stat_sessid=fdp2bsh98e99i5peod9tdl6687; PHPSESSID=57f1cro7l9jtjq8365jshta8u3; PHPSESSID=65t6tfkegng9dkgjoejbhks6o6; had_quiz_183906=1499061360000; http_tK_cache=49886aa55e8bd6f5d517dff95b091bfdfa5c8c9c; cur_ck_time=1499243625; ck_request_key=0Hl7pvad%2F3KjpqcZnyKi1skj8cK4P2tiAfX4bgLu580%3D; passport=183906%09u_464246026497%09A19RUQ8AVlUPBwAGAlJZWVZWVwdQVwJQAFJRBA0EVAY%3Dca1c8e9b4c; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Du_464246026497; rz_rem_u_p=xweZIQNnUe1WsOPckXHPJTkIbbUkr9a%2B7nrx3MRBXWo%3D%24YXbAptyqBXD0LrGBP9wY4t%2FYfuCiYkjq16HL2GKS1Nk%3D; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1496893693,1498549384; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1499247294; rz_token_6658=b000f401ffead9f87ae62d5ee17a8eab.1499247293; passportmall=UwcHDFZWbxdsAFAFCg0DBlcCDAEB827c2e5f9b; autologin_status=0",

        }

        self._simuwang_data_urls = {
            # net asset value url
            "navs": "http://dc.simuwang.com/index.php?m=Data2&c=Chart&a=jzdb_fund&muid=183906&fund_id=%s"
        }

    def headers(self):
        return self._simuwang_access_headers

    def url(self, url):
        return self._simuwang_data_urls.get(url)


class Loader(loader.Loader):
    """
        loader for fund data at simuwang
    """
    def __init__(self):
        # initialize the loader's context
        loader.Loader.__init__(self, Context())

    def all(self, code):
        pass

    def navs(self, code):
        """
            load fund nav from simuwang by its code in simuwang.
        :param code:
        :return:
        """
        # fetch & parse the url data for fund @code
        url =  self.url("navs") % (code)
        json_data = json.loads(requests.get(url, headers=self.headers()).text)

        # extract fund name
        name = json_data.get('title')[0]

        # extract fund data from json content
        navtbl = dtl.table([['date', 'nav', 'aav']]).extend(dtl.table(cols=([json_data.get('categories'), dtl.floats(json_data.get('nav_list')), dtl.floats(json_data.get('nav_list'))])))

        return navtbl

