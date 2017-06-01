'''
    performance attribution algorithms
'''
import re, xlrd

class BLoader:
    '''
        benchmark data loader
    '''
    def __init__(self, source_file):
        self.source_file = source_file

    def load(self):
        '''
            load benchmark data from excel file
        :return:
        '''
        iindexs, sindustries = {}, {}

        file = xlrd.open_workbook(self.source_file)
        for name in file.sheet_names():
            sheet = file.sheet_by_name(name)
            if name == 'industry':
                for rowx in range(sheet.nrows):
                    scode, icode = sheet.row_values(rowx)
                    sindustries[scode] = icode
            elif re.match('[\d]+-[\d]+-[\d]+', name):
                for rowx in range(sheet.nrows):
                    code, weight, open_index, close_index = sheet.row_values(rowx)
                    iindexs[name] = {code:[weight, open_index, close_index]}
            else:
                pass

        return self

class PLoader:
    '''
        portfolio data loader
    '''
    def __init__(self, source_file):
        self.source_file = source_file

    def load(self):
        '''
            load portfolio data form excel file
        :return:
        '''
        holdings = {}

        file = xlrd.open_workbook(self.source_file)
        for name in file.sheet_names():
            sheet = file.sheet_by_name(name)
            if re.match('[\d]+-[\d]+-[\d]+', name):
                for rowx in range(sheet.nrows):
                    code, weight, open_price, close_price = sheet.row_values(rowx)
                    holdings[name] = {code:[weight, open_price, close_price]}
            else:
                pass

        return holdings


class Benchmark:
    '''
        benchmark information for brinson analysis
    '''
    def __init__(self):
        #daily industry indexs: date->{code->[weight, open-index, close-index]}
        self.iindexs = None
        #stock industries in benchmark: stock code->industry code
        self.sindustries = None


    def load(self, loader):
        '''
            load benchmark data for brinson
        :param loader:
        :return:
        '''
        self.iindexs, self.sindustries = loader.load()
        return self


class Portfolio:
    '''
        portfolio information for analysis
    '''
    def __init__(self):
        #daily stock holdings after daily transaction ends: date->{code->[weight, open-price, close-price]}
        self.holdings = None

    def load(self, loader):
        '''
            load portfolio data for brinson
        :param loader:
        :return:
        '''
        self.holdings = loader.load()
        return self

class Brinson:
    '''
        brinson performance attribution algorithm
    '''
    def __init__(self):
        #benchmark for portfolio
        self.benchmark = None
        #portfolio to be attributed
        self.portfolio = None

    def init(self, benchmark, portfolio):
        #benchmark for portfolio
        self.benchmark = benchmark
        #portfolio to be attributed
        self.portfolio = portfolio

        return self

    def analyse(self):
        '''
            brinson analyse for portfolio with specified benchmark
        :return: [benchmark return, portfolio return, excess return, asset selection return, stock selection return, interaction return]
        '''
        attribution_results = []
        for date, stocks in self.portfolio.holdings:

            #compute benchmark return as q1
            q1 = 0.0
            for weight, open_index, close_index in self.benchmark.iindexs[date].values():
                q1 += weight*(close_index-open_index)/open_index
            br = q1

            #compute portfolio return as q4
            q4 = 0.0
            for weight, open_price, close_price in stocks.values():
                q4 += weight*(close_price-open_price)/open_price
            pr = q4

            #compute industry and stock selection as q2 & q3
            q2, q3 = 0.0, 0.0
            for scode, holds in stocks.items():
                sweight, open_price, close_price = holds
                icode = self.benchmark.sindustries[scode]
                iweight, open_index, close_index = self.benchmark.iindexs[date][icode]

                q2 += sweight*(close_index-open_index)/open_index
                q3 += iweight*(close_price-open_price)/open_price

            #compute attribution for portfilio
            ar = q2-q1
            sr = q3-q1
            ir = q4-q3-q2+q1
            tr = q4-q1

            #add to results
            attribution_results.append([br, pr, tr, ar, sr, ir])

        return attribution_results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "Usage: python perf.py <benchmark file> <portfolio file>"
        exit()

    benchmark = Benchmark().load(BLoader(sys.argv[1]))
    portfolio = Portfolio().load(PLoader(sys.argv[2]))

    results = Brinson().init(benchmark, portfolio).analyse()
    for result in results:
        print result