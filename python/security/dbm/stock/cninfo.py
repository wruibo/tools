"""
    stock data from cninfo, web site:
    http://www.cninfo.com.cn/
"""
import utl, time


class context:
    """
        context data for access caifuqiao
    """
    # access headers for www.cninfo.com.cn
    _cninfo_access_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36",
        "Host": "www.cninfo.com.cn",
        "Referer": "http://www.cninfo.com.cn/cninfo-new/index",
    }


    _cninfo_data_urls = {
        # net asset value url
        "finance_income": "http://www.cninfo.com.cn/cninfo-new/data/download",
        "finance_balance": "http://www.cninfo.com.cn/cninfo-new/data/download",
        "finance_cashflow": "http://www.cninfo.com.cn/cninfo-new/data/download",
        "quotation_daily": "http://www.cninfo.com.cn/cninfo-new/data/download"

    }

    @staticmethod
    def headers():
        return context._cninfo_access_headers

    @staticmethod
    def url(url):
        return context._cninfo_data_urls.get(url)


class loader:
    """
        stock data request from www.cninfo.com.cn
    """
    def __init__(self, market, code):
        self._market = market
        self._code = code

    def finance_income(self, starty=None, endy=None):
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
        url = context.url("finance_income")

        # post form data
        form_data = {
            "market": self._market,
            "type": "lrb",
            "code": self._code,
            "orgid": "gs%s%s" % (self._market, self._code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = utl.net.http.client(url, data=form_data, headers=context.headers()).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        incomes = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if incomes is None:
                    incomes = [row]

                if is_header:
                    is_header = False
                    continue

                incomes.append(row)

        return incomes[1:]

    def finance_balance(self, starty=None, endy=None):
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
        url = context.url("finance_balance")

        # post form data
        form_data = {
            "market": self._market,
            "type": "fzb",
            "code": self._code,
            "orgid": "gs%s%s" % (self._market, self._code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = utl.net.http.client(url, data=form_data, headers=context.headers()).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        balances = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if balances is None:
                    balances = [row]

                if is_header:
                    is_header = False
                    continue

                balances.append(row)

        # return parse result for profit
        return balances

    def finance_cashflow(self, starty=None, endy=None):
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
        url = context.url("finance_cashflow")

        # post form data
        form_data = {
            "market": self._market,
            "type": "llb",
            "code": self._code,
            "orgid": "gs%s%s" % (self._market, self._code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = utl.net.http.client(url, data=form_data, headers=context.headers()).post().unzip().decodes('gb2312').csvs().data

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

    def quotation_daily(self, starty=None, endy=None):
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
        url = context.url("quotation_daily")

        # post form data
        form_data = {
            "market": self._market,
            "type": "hq",
            "code": self._code,
            "orgid": "gs%s%s" % (self._market, self._code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = utl.net.http.client(url, data=form_data, headers=context.headers()).post().unzip().decodes('gb2312').csvs().data

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
    incomes = loader('sz', '000001').finance_income(0, 2017)
    balances = loader('sz', '000001').finance_balance(0, 2017)
    cashflows = loader('sz', '000001').finance_cashflow(0, 2017)
    quotations = loader('sz', '000001').quotation_daily(0, 2017)

    print("income statement-")
    for row in incomes:
        print(row)

    print("balance sheet-")
    for row in balances:
        print(row)

    print("cashflows-")
    for row in cashflows:
        print(row)

    print("quotations-")
    for row in quotations:
        print(row)
