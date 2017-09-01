"""
    fund data from simuwang, site:
        http://www.simuwang.com/
"""
import atl, dtl, dbm


class context:
    """
        context data for access simuwang
    """
    # access headers for simuwang
    _simuwang_access_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host": "dc.simuwang.com",
        "Cookie": "regsms=1489648164000; guest_id=1489648267; PHPSESSID=8a438266a0f5v80vofmjvqsir3; stat_sessid=an73u6hiq1jdisk9jl43ehkaq4; cur_ck_time=1503905488; ck_request_key=N0cxI8j0ySArlHaTA6KzhjmBWyGIfSCAr7ECXGJ7OEQ%3D; http_tK_cache=761574bdd2f48eb02637c4a3a503b8d6e16f7b2c; passport=183906%09u_464246026497%09A19RUQ8AVlUPBwAGAlJZWVZWVwdQVwJQAFJRBA0EVAY%3Dca1c8e9b4c; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Du_464246026497; rz_rem_u_p=xweZIQNnUe1WsOPckXHPJTkIbbUkr9a%2B7nrx3MRBXWo%3D%24YXbAptyqBXD0LrGBP9wY4t%2FYfuCiYkjq16HL2GKS1Nk%3D; PHPSESSID=4mqk2jfauv9it8r71lu8u445t3; had_quiz_183906=1503905491000; rz_token_6658=994e945ad73e12273506d34344be16b6.1503909454; autologin_status=0; passportmall=UwcHDFZWbxdsAFAFCg0DBlcCDAEB827c2e5f9b; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1502869164,1503909454; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1503909500",

    }

    _simuwang_data_urls = {
        # net asset value url
        "nav": "http://dc.simuwang.com/index.php?m=Data2&c=Chart&a=jzdb_fund&muid=183906&fund_id=%s"
    }

    @staticmethod
    def headers():
        return context._simuwang_access_headers

    @staticmethod
    def url(url):
        return context._simuwang_data_urls.get(url)


class loader:
    """
        loader for fund data at simuwang
    """
    def __init__(self, code):
        self._code = code

    def nav(self):
        """
            load fund nav from simuwang by its code in simuwang.
        data format:
            [
                [date, nav, aav],
                [...]
            ]
        :param code: str, fund code in simuwang
        :return: matrix, nav records
        """
        # fetch & parse the url data for fund @code
        url =  context.url("nav") % (self._code)

        # get json data from url
        json_data = dbm.core.rda.http(url, headers=context.headers()).xget().json().data
        #json_data = dbm.rqst.getjson(url, headers=context.headers())

        # extract fund name
        name = json_data.get('title')[0]

        # extract fund data from json content
        return dtl.matrix.transpose([dtl.cast.cast(json_data.get('categories'), dtl.time.date, "%Y-%m-%d"), dtl.cast.floats(json_data.get('nav_list')), dtl.cast.floats(json_data.get('nav_list'))])
