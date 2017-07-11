"""
    jensen ratio in CAMP model, also call alpha
"""

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