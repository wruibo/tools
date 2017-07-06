"""
    loader for fund data
"""
import requests, json

from pf import fund
from util import type, mtx


class LoaderSimuwang:
    URL_FORMAT = "http://dc.simuwang.com/index.php?m=Data2&c=Chart&a=jzdb_fund&muid=183906&fund_id=%s"
    HEADERS = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host":"dc.simuwang.com",
        "Cookie":"regsms=1489648164000; guest_id=1489648267; stat_sessid=fdp2bsh98e99i5peod9tdl6687; PHPSESSID=57f1cro7l9jtjq8365jshta8u3; PHPSESSID=65t6tfkegng9dkgjoejbhks6o6; had_quiz_183906=1499061360000; http_tK_cache=49886aa55e8bd6f5d517dff95b091bfdfa5c8c9c; cur_ck_time=1499243625; ck_request_key=0Hl7pvad%2F3KjpqcZnyKi1skj8cK4P2tiAfX4bgLu580%3D; passport=183906%09u_464246026497%09A19RUQ8AVlUPBwAGAlJZWVZWVwdQVwJQAFJRBA0EVAY%3Dca1c8e9b4c; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Du_464246026497; rz_rem_u_p=xweZIQNnUe1WsOPckXHPJTkIbbUkr9a%2B7nrx3MRBXWo%3D%24YXbAptyqBXD0LrGBP9wY4t%2FYfuCiYkjq16HL2GKS1Nk%3D; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1496893693,1498549384; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1499247294; rz_token_6658=b000f401ffead9f87ae62d5ee17a8eab.1499247293; passportmall=UwcHDFZWbxdsAFAFCg0DBlcCDAEB827c2e5f9b; autologin_status=0",

    }
    def __init__(self):
        pass

    def load(self, code):
        """
            load fund nav from simuwang by its code in simuwang.
        :param code:
        :return:
        """
        # fetch & parse the url data for fund @code
        url = self.URL_FORMAT % (code)
        json_data = json.loads(requests.get(url, headers=self.HEADERS).text)

        # extract fund name
        name = json_data.get('title')[0]

        # extract fund data from json content
        navs = mtx.rotate([json_data.get('categories'), type.floats(json_data.get('nav_list')), type.floats(json_data.get('nav_list'))])

        return fund.Fund(code, name, navs)


def load(code):
    return LoaderSimuwang().load(code)

if __name__ == "__main__":
    from ds import matrix
    from prr import sharpe

    print(load("HF000010YC"))
    codes = ["HF000010YC", "HF00000SCO", "HF00000Z6H", "HF00001BPV", "HF0000137H"]
    sharpes = []
    for code in codes:
        f = load(code)
        mnavs = matrix.Matrix().init(rows=f.navs)
        sharpes.append(sharpe.Sharpe(mnavs, 1, "%Y-%m-%d", 3, 0.016).run(True))

    print(codes)
    print(sharpes)
