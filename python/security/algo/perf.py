'''
    performance attribution algorithms
'''
import csv


class BLoader:
    '''
        benchmark data loader
    '''
    def __init__(self):
        pass

    def load(self, source):
        '''
            load benchmark data from @source, source may be the following formats:
        file:
            csv file split with ',', content with:
             date, value
             2017-05-12, 3214
             ...,...
        list:
            [
                ['2017-05-12', 3214]
                [...,...]
            ]
        dict:
            {
                '2017-05-12':3214,
                ...,...
            }

        :param source: file/list/dict
        :return:
        '''
        if isinstance(source, dict):
            self.indexs = source
        elif isinstance(source, list):
            for index in source:
                self.indexs[index[0]] = index[1]
        elif isinstance(source, str):
            for line in open(source, 'r'):
                date, value = line.split(',')
                self.indexs[date] = value
        else:
            pass

        return self

    def load_benchmark(self, index):
        pass

    def load_industry(self, indexs):
        pass


class PLoader:
    '''
        portfolio data loader
    '''
    def __init__(self):
        pass


class Benchmark:
    '''
        benchmark information for brinson analysis
    '''
    def __init__(self):
        #benchmark index: date->[open-price, close-price]
        self.bindexs = None
        #industry index: code->{date->[open-price, close-price]}
        self.iindexs = None
        #industry weight in benchmark: industry code->weight
        self.iweights = None
        #stock industries in benchmark: stock code->industry code
        self.sindustries = None


    def load(self, loader):
        '''
            load benchmark data for brinson
        :param loader:
        :return:
        '''
        self.bindexs, self.iindexs, self.iweights, self.sindustries = loader.load()
        return self


class Portfolio:
    '''
        portfolio information for analysis
    '''
    def __init__(self):
        #daily equity holdings after daily transaction ends: date->{code->[holds, open-price, close-price]}
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
        :return:
        '''
        attribution_results = []
        for date, stocks in self.portfolio.holdings:
            #compute benchmark return as q1
            q1 = (self.benchmark.bindexs[date][1] - self.benchmark.bindexs[date][0]) / self.benchmark.bindexs[date][0]

            #compute portfolio return as q4
            openv, closev = 0, 0
            for count, open, close in stocks.values():
                 openv += count*open
                 closev += count*close
            q4 = (closev - openv) / openv

            #compute industry selection return
            for code, holds in stocks.items():
                pass

            #compute stock selection return
            #compute interaction return

        return attribution_results