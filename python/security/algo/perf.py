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
            load benchmark data from excel file, file format:
        sheet name:
            yyyy-mm--dd
        sheet columns
            code, weight, open, close
        :return:
        '''
        prices = {}

        file = xlrd.open_workbook(self.source_file)
        for date in file.sheet_names():
            sheet = file.sheet_by_name(date)
            if re.match(r'[\d]+-[\d]+-[\d]+', date):
                if not self.check(sheet):
                    raise "benchmark file format is not valid."
                prices[date] = {}
                for rowx in range(1, sheet.nrows):
                    code, weight, open, close = sheet.row_values(rowx)
                    prices[date][code] = [weight, open, close]
            else:
                pass

        return prices

    def check(self, sheet):
        '''
            check sheet format
        :param sheet:
        :return:
        '''
        if sheet.nrows > 0:
            code, weight, open, close = sheet.row_values(0)
            if code=='code' and weight=='weight' and open=='open' and close=='close':
                return True
        return False


class PLoader:
    '''
        portfolio data loader
    '''
    def __init__(self, source_file):
        self.source_file = source_file

    def load(self):
        '''
            load portfolio data form excel file, file format
        sheet name:
            yyyy-mm--dd
        sheet columns
            code, category weight, open, close
        :return:
        '''
        prices = {}

        file = xlrd.open_workbook(self.source_file)
        for date in file.sheet_names():
            sheet = file.sheet_by_name(date)
            if re.match('[\d]+-[\d]+-[\d]+', date):
                if not self.check(sheet):
                    raise "portfolio file format is not valid."
                prices[date] = {}
                for rowx in range(1, sheet.nrows):
                    code, category, weight, open, close = sheet.row_values(rowx)
                    prices[date][code] = [category, weight, open, close]
            else:
                pass

        return prices

    def check(self, sheet):
        '''
            check sheet format
        :param sheet:
        :return:
        '''
        if sheet.nrows > 0:
            code, category, weight, open, close = sheet.row_values(0)
            if code=='code' and category=='category' and weight=='weight' and open=='open' and close=='close':
                return True
        return False


class Benchmark:
    '''
        benchmark information for brinson analysis
    '''
    def __init__(self):
        #daily benchmark prices: date->{code->[weight, open, close]}
        self.prices = None

    def load(self, loader):
        '''
            load benchmark data for brinson
        :param loader:
        :return:
        '''
        self.prices = loader.load()
        return self


class Portfolio:
    '''
        portfolio information for analysis
    '''
    def __init__(self):
        #daily portfolio prices: date->{code->[category, weight, open, close]}
        self.prices = None

    def load(self, loader):
        '''
            load portfolio data for brinson
        :param loader:
        :return:
        '''
        self.prices = loader.load()
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
        for date, property in self.portfolio.prices.items():

            #compute benchmark return as q1
            q1 = 0.0
            for weight, open, close in self.benchmark.prices[date].values():
                q1 += weight*(close-open)/open
            br = q1

            #compute industry selection as q2, stock selection as q3, portfolio return as q4
            q2, q3, q4 = 0.0, 0.0, 0.0
            for category, pweight, popen, pclose in property.values():
                cweight, copen, cclose = self.benchmark.prices[date][category]
                q2 += pweight * (cclose - copen) / copen
                q3 += cweight * (pclose - popen) / popen
                q4 += pweight*(pclose-popen)/popen

            pr = q4

            #compute attribution for portfilio
            ar = q2-q1
            sr = q3-q1
            ir = q4-q3-q2+q1
            tr = q4-q1

            #add to results
            attribution_results.append([date, br, pr, tr, ar, sr, ir])

        return attribution_results

if __name__ == "__main__":
    import sys
    usage = "Usage: python perf.py <benchmark file> <portfolio file>\n" \
            "benchmark file format:\n" \
            "   sheet name: yyyy-mm--dd\n" \
            "   sheet columns: code, weight, open, close\n" \
            "portfolio file format:\n" \
            "   sheet name: yyyy-mm--dd\n" \
            "   sheet columns: code, category, weight, open, close\n"

    if len(sys.argv) != 3:
        print(usage)
        exit()

    benchmark = Benchmark().load(BLoader(sys.argv[1]))
    portfolio = Portfolio().load(PLoader(sys.argv[2]))

    print("date, br, pr, tr, ar, sr, ir")
    results = Brinson().init(benchmark, portfolio).analyse()
    for result in results:
        print(result)