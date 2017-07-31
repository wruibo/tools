import matplotlib.pyplot as plot

def draw(xarray, yarrays, xlable = None, ylable = None):
    """

    :param xArray:
    :param yArrays:
    :param xLable:
    :param yLable:
    :return:
    """

    for yArray in yArrays:
        plot.plot(xArray, yArray)

    plot.xlabel(xLable)
    plot.ylabel(yLable)

    plot.show()