'''
    portfolio performance atrribution analysis using brinson model
'''

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