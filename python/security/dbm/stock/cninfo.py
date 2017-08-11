"""
    stock data from cninfo, web site:
    http://www.cninfo.com.cn/
"""
import dbm, dtl, time


class cninfo:
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

    def profit1(self, market, code, starty=None, endy=None):
        """
            profit of company
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
            "orgid":"gs%s%s"%(market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        profits = []
        for name, csv in csvs:
            skip_header = True
            for row in csv:
                if skip_header:
                    skip_header = False
                    continue

                profit = dtl.stock.profit()

                # company relate items
                profit.company_code = row[0].strip()
                profit.company_name = row[1]

                # report relate items
                profit.report_date_notice = row[2]
                profit.report_date_start = row[3]
                profit.report_date_end = row[4]
                profit.report_year = row[5]
                profit.report_merge_type = row[6]
                profit.report_source = row[7]

                # income/cost/profit items
                profit.income_operating_total = row[8]
                profit.income_operating = row[9]

                profit.cost_operating_total = row[10]
                profit.cost_operating = row[11]
                profit.cost_tax_and_annex = row[12]
                profit.cost_sales = row[13]
                profit.cost_management = row[14]
                profit.cost_explorer = row[15]
                profit.cost_finance = row[16]
                profit.cost_asset_impairment = row[17]

                profit.ic_fair_value_changes = row[18]

                profit.income_invest = row[19]
                profit.income_invest_joint_venture = row[20]
                profit.income_exchange_gains = row[21]

                profit.ic_other_subject1 = row[22]

                profit.profit_operating = row[23]

                profit.income_subsidy = row[24]
                profit.income_non_operating = row[25]

                profit.cost_non_operating = row[26]
                profit.cost_non_current_asset_dispose = row[27]

                profit.ic_other_subject2 = row[28]

                profit.profit_total = row[29]

                profit.cost_income_tax = row[30]

                profit.ic_other_subject3 = row[31]

                profit.profit_net = row[32]
                profit.profit_belongto_parent_company = row[33]

                profit.ic_minority_interest = row[34]

                profit.profit_per_share = row[35]
                profit.profit_base_per_share = row[36]
                profit.profit_dilution_per_share = row[37]

                profit.profit_other_comprehensive = row[38]
                profit.profit_comprehensive_total = row[39]
                profit.profit_comprehensive_belongto_parent_company = row[40]
                profit.profit_comprehensive_belongto_minority_interest = row[41]

                profit.income_interest = row[42]
                profit.income_premium = row[43]
                profit.income_service_charge_and_commission = row[44]
                profit.cost_interest = row[45]
                profit.cost_service_charge_and_commission = row[46]
                profit.cost_surrender_value = row[47]
                profit.cost_compensation_payout = row[48]

                profit.cost_insurance_reserve_fund = row[49]
                profit.cost_insurance_expense = row[50]
                profit.cost_reinsurance = row[51]
                profit.income_non_current_asset_dispose = row[52]

                profits.append(profit)


        # return parse result for profit
        return profits

    def profit(self, market, code, starty=None, endy=None):
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
            "type": "lrb",
            "code": code,
            "orgid": "gs%s%s" % (market, code),
            "minYear": str(starty),
            "maxYear": str(endy)
        }

        # get csv data from url
        csvs = dbm.core.rda.http(url, data=form_data, headers=self._headers).post().unzip().decodes('gb2312').csvs().data

        # parse csv data
        profits = None
        for name, csv in csvs:
            is_header = True
            for row in csv:
                if profits is None:
                    profits = [row]

                if is_header:
                    is_header = False
                    continue

                profits.append(row)

        # return parse result for profit
        return profits

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
