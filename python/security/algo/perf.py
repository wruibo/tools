'''
    performance attribution algorithms
'''


class Benchmark:
    '''
        benchmark information for brinson analysis
    '''
    def __init__(self):
        #benchmark index, date->index value
        self.index ={}
        #industry index, code->{date->index value}
        self.industry = {}

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


class Portfolio:
    '''
        portfolio information for analysis
    '''
    def __init__(self):
        pass


class Brinson:
    '''
        brinson performance attribution algorithm
    '''
    def __init__(self):
        pass

    def init(self, benchmark, industry, portfolio):
        # benchmark for portfolio
        self.benchmark = benchmark
        # industry for benchmark
        self.industry = industry
        # portfolio to be attributed
        self.portfolio = portfolio

        return self

    def analyse(self):
        pass