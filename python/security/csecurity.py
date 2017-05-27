import sys, math, datetime
import cutil, carray, cmath, cmatrix

'''
    security algorithms

glossary:
    price(s) - asset price(s)
    revenue(s) - asset revenue rate(s)
    rf - risk free return rate
    rm - market return rate
'''

def Revenue(datePrices, baseDatePrice = None, strDateFormat = "%Y%m%d"):
    '''
    get the year revenue sequence from (date, price) sequence, where the date price sequence
    is ordered by date before-to-future
    :param datePrices: list,
        list of list, [[date1, price1], [date2, price2], ...],
        where
        date1<date2
    :param baseDatePrice: list, [date, price], base date price point, use @datePrice[0] as @baseDatePrice when
        it is None
    :param strDateFormat: string, date format of the @datePrices
    :return: list,
        float in list, revenue sequence, [revenue1, revenue2, ...],
        where:
        revenue(i) = 365*(price(i) - price(i-1)) / (date(i) - date(i-1))
    '''
    dates = cmatrix.ExtractColumn(datePrices, 1)
    prices = cutil.ConvertType(cmatrix.ExtractColumn(datePrices, 2), float)

    if baseDatePrice is None:
        baseDatePrice = cutil.DateBefore(dates[0], 1, strDateFormat), prices[0]

    dates = carray.LeftShiftSub(dates, baseDatePrice[0], cutil.DaysBetween, strDateFormat)
    prices = carray.CycleGrowthRate(prices, baseDatePrice[1])

    print dates
    print prices

    return carray.M(carray.DivArray(prices, dates), 365)

def SlowMaxDrawdown(prices):
    '''
    compute the drawdown of the given prices, using normal algorithm:
        prices = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param prices: list, float in list, with sequence of price values
    :return: [max-drawdown, position i, value i, position j, value j] of the list prices
    '''
    pMax, vMax, pMin, vMin, drawdown = None, None, None, None, None

    i = j = 0
    while i < len(prices):
        j = i + 1
        while j < len(prices):
            ijDrawdown = (prices[j] - prices[i]) / prices[i]
            if (drawdown is None and ijDrawdown<0.0) or ijDrawdown < drawdown:
                pMax, vMax, pMin, vMin, drawdown = i, prices[i], j, prices[j], ijDrawdown
            j = j + 1
        i = i + 1

    return drawdown, pMax, vMax, pMin, vMin


def FastMaxDrawdown(prices):
    '''
    compute the drawdown of the given prices, using fast algorithm:
        prices = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param prices: list, float in list, with sequence of price values
    :return: [max-drawdown, position i, value i, position j, value j] of the list prices
    '''
    pMax, vMax, pMin, vMin, drawdown = None, None, None, None, None
    iPos, iValue, jPos, jValue, ijDrawdown = None, None, None, None, None

    i = j = 0
    while i + 1 < len(prices) and j + 1 < len(prices):
        if prices[i] < prices[i+1]:
            i = i + 1
            continue
        j = i + 1
        while j + 1 < len(prices):
            if prices[j] < prices[j-1] and prices[j] <= prices[j+1]:
                if ijDrawdown is None or prices[j] < jValue:
                    iPos, iValue, jPos, jValue, ijDrawdown = i, prices[i], j, prices[j], (prices[j] - prices[i]) / prices[i]

                if drawdown is None or ijDrawdown < drawdown:
                    pMax, vMax, pMin, vMin, drawdown = iPos, iValue, jPos, jValue, ijDrawdown
            else:
                if prices[j] > prices[i]:
                    i = j
                    iPos, iValue, jPos, jValue, ijDrawdown = None, None, None, None, None
                    break
            j = j + 1

    if i < j < len(prices):
        if ijDrawdown is None or prices[j] < jValue:
            iPos, iValue, jPos, jValue, ijDrawdown = i, prices[i], j, prices[j], (prices[j] - prices[i]) / prices[i]

        if drawdown is None or ijDrawdown < drawdown:
            pMax, vMax, pMin, vMin, drawdown = iPos, iValue, jPos, jValue, ijDrawdown

    return drawdown, pMax, vMax, pMin, vMin

def MaxDrawdown(prices):
    '''
    compute the drawdown of the given prices, using fast algorithm:
        prices = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param prices: list, float in list, with sequence of price values
    :return: [max-drawdown, position i, value i, position j, value j] of the list prices
    '''
    return FastMaxDrawdown(prices)

def SharpeRatio(revenues, rf):
    '''
    compute sharpe ratio with the given revenues list, formula:
        AssetsSharpeRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / StandardDeviation(AssetsRevenues)
    constraint:
        the interval of assets revenue sample interval must be the same as risk free return rate interval,
    normally we can use the year return rate for assets and risk free return

    :param revenues: list, interval revenue rate list, example:
        [0.023, 0.032, 0.04, ...]
    :param rf: float, interval risk free return rate, same interval with @revenues
    :return: float, sharpe ratio fo the assets
    '''
    #use average of revenues as expect assets revenue
    expect = carray.Average(revenues)

    #standard deviation of revenues
    sd = cmath.StandardDeviation(revenues)

    return (expect - rf) / sd

def BetaFactor(assetsRevenues, marketRevenues):
    '''
    compute the beta factor of the given assets, formula:
       AssetsBetaFactor = Cov(AssetsRevenues, MarketRevenues)/Variance(MarketRevenues)
    constraint:
        intput @assetRevenues and @marketRevenues must be one-to-one correspondence
    :param assetsRevenues: list, float in list, assets sample revenue list
    :param marketRevenues: list, float in list, market sample revenue list, correspond with @assetsRevenues
    :return: float, beta factor of assets
    '''

    if len(assetsRevenues) != len(marketRevenues):
        raise "assets revenue sequence must be one-to-one correspondence with the market revenue sequence!"

    return cmath.Covariance(assetsRevenues, marketRevenues) / cmath.Variance(marketRevenues)

def TreynorRatio(assetsRevenues, marketRevenues, rf):
    '''
     compute the Treynor ratio of the given assets, formula:
        AssetsTreynorRatio = (ExpectAssetsRevenue - RiskFreeReturnRate) / AssetsBetaFactor
    constraint:
        intput @assetRevenues and @marketRevenues must be one-to-one correspondence

    :param assetsRevenues: list, float in list, assets sample revenue list
    :param marketRevenues: list, float in list, market sample revenue list, correspond with @assetsRevenues
    :param rf:float, interval risk free return rate, same interval with @assetsRevenues and @assetsRevenues
    :return: float, beta factor of assets
    '''
    if len(assetsRevenues) != len(marketRevenues):
        raise "assets revenue sequence must be one-to-one correspondence with the market revenue sequence!"

    #use average of revenues as expect assets revenue
    expect = carray.Average(assetsRevenues)

    #beta factor of assets
    beta = BetaFactor(assetsRevenues, marketRevenues)

    return (expect - rf) / beta

def JensenRatio(assetsRevenues, marketRevenues, rf):
    '''
    compute the Jensen ratio of given assets, the Jensen ration also called alpha value of assets, formula:
        AssetsJensenRatio = AssetsExpectRevenue - [rf + AssetsBetaFactor*(MarketExpectRevenue - RiskFreeReturnRate)]
    constraint:
        intput @assetRevenues and @marketRevenues must be one-to-one correspondence

    :param assetsRevenues: list, float in list, assets sample revenue list
    :param marketRevenues: list, float in list, market sample revenue list, correspond with @assetsRevenues
    :param rf:float, interval risk free return rate, same interval with @assetsRevenues and @assetsRevenues
    :return: float, Jensen ratio of assets
    '''
    if len(assetsRevenues) != len(marketRevenues):
        raise "assets revenue sequence must be one-to-one correspondence with the market revenue sequence!"

    assetsExpect = carray.Average(assetsRevenues)
    marketExpect = carray.Average(marketRevenues)

    assetsBetaFactor = BetaFactor(assetsRevenues, marketRevenues)

    return assetsExpect - (rf + assetsBetaFactor * (marketExpect - rf))
