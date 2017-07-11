import matplotlib.pyplot as plot

def PlotLine(xArray, yArrays, xLable = None, yLable = None):
    '''
    plot line with @x array & y arrays
    :param xArray:
    :param yArrays:
    :param xLable:
    :param yLable:
    :return:
    '''
    for yArray in yArrays:
        plot.plot(xArray, yArray)

    plot.xlabel(xLable)
    plot.ylabel(yLable)

    plot.show()