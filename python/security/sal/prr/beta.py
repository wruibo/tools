"""
    beta factor in CAMP model
"""

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