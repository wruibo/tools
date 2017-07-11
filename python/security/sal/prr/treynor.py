"""
    treynor ratio from CAMP model
"""

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