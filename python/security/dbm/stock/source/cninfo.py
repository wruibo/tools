"""
    stock data from cninfo, web site:
    http://www.cninfo.com.cn/
"""
from .dao import Dao


class CNInfo(Dao):
    """
        stock data request from www.cninfo.com.cn
    """
    # access headers for www.cninfo.com.cn
    _headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host": "www.cninfo.com.cn",
        "Referer": "http://www.cninfo.com.cn/cninfo-new/index",
    }

    def __init__(self):
        pass

    def _profit(self, market, code, starty=None, endy=None):
        """
            get profit data from remote
        :param market: str, sz or sh
        :param code: str, code of company in stock market
        :param starty: int, start year for profit
        :param endy: int, end year for profit
        :return: obj
        """
        # configure the time range of profit
        if starty is None: starty = 0
        if endy is None: endy = time.gmtime().tm_year

        # url for profit on website
        url = "http://www.cninfo.com.cn/cninfo-new/data/download"

        # post form data
        form_data = {
            "market": market,
            "type": "lrb",
            "code": code,
            "orgid": "gs%s%s" % (market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        records = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if records is None:
                    records = [row]

                if is_header:
                    is_header = False
                    continue

                records.append(row)

        records = dtl.matrix.transpose(records[1:])

        return records

    def profit(self, market, code, starty=None, endy=None):
        """

        :param market:
        :param code:
        :param starty:
        :param endy:
        :return:
        """

        records = self._profit(market, code, starty, endy)
        profit = dtl.stock.finance.profit(date=records[5], total=records[19], operating=records[23], net=records[32])

        # return parse result for profit
        return profit


    def asset(self, market, code, starty=None, endy=None):
        """
            assets and liabilities of company
        :param market: str, sz or sh
        :param code: str, code of company in stock market
        :param starty: int, start year for profit
        :param endy: int, end year for profit
        :return: obj
        """
        # configure the time range of profit
        if starty is None: starty = 0
        if endy is None: endy = time.gmtime().tm_year

        # url for profit on website
        url = "http://www.cninfo.com.cn/cninfo-new/data/download"

        # post form data
        form_data = {
            "market": market,
            "type": "fzb",
            "code": code,
            "orgid": "gs%s%s" % (market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        assets = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if assets is None:
                    assets = [row]

                if is_header:
                    is_header = False
                    continue

                assets.append(row)

        # return parse result for profit
        return assets

    def cashflow(self, market, code, starty=None, endy=None):
        """
            cash flow of company
        :param market: str, sz or sh
        :param code: str, code of company in stock market
        :param starty: int, start year for profit
        :param endy: int, end year for profit
        :return: obj
        """
        # configure the time range of profit
        if starty is None: starty = 0
        if endy is None: endy = time.gmtime().tm_year

        # url for cash flow on website
        url = "http://www.cninfo.com.cn/cninfo-new/data/download"

        # post form data
        form_data = {
            "market": market,
            "type": "llb",
            "code": code,
            "orgid": "gs%s%s" % (market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        cashflows = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if cashflows is None:
                    cashflows = [row]

                if is_header:
                    is_header = False
                    continue

                cashflows.append(row)

        # return parse result for cash flow
        return cashflows

    def quotation_daily(self, market, code, starty=None, endy=None):
        """
            daily quotation of company
        :param market: str, sz or sh
        :param code: str, code of company in stock market
        :param starty: int, start year for profit
        :param endy: int, end year for profit
        :return: obj
        """
        # configure the time range of quotations
        if starty is None: starty = 0
        if endy is None: endy = time.gmtime().tm_year

        # url for cash flow on website
        url = "http://www.cninfo.com.cn/cninfo-new/data/download"

        # post form data
        form_data = {
            "market": market,
            "type": "hq",
            "code": code,
            "orgid": "gs%s%s" % (market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        quotations = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if quotations is None:
                    quotations = [row]

                if is_header:
                    is_header = False
                    continue

                quotations.append(row)

        # return parse result for daily quotations
        return quotations


if __name__ == "__main__":
    profits = cninfo().profit('sz', '000001', 0, 2017)
    assets = cninfo().asset('sz', '000001', 0, 2017)
    cashflows = cninfo().cashflow('sz', '000001', 0, 2017)
    quotations = cninfo().quotation_daily('sz', '000001', 0, 2017)

    print("profits-")
    for row in profits:
        print(row)

    print("assets-")
    for row in assets:
        print(row)

    print("cashflows-")
    for row in cashflows:
        print(row)

    print("quotations-")
    for row in quotations:
        print(row)
