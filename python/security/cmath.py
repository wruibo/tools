'''
    useful normal mathematics algorithms
'''
import math

def Average(values):
    '''
    compute average of sample values
    :param values: list, list of sample values
    :return: float, average of sample values
    '''
    return sum(values) / len(values)

def Variance(values):
    '''
    compute variance of sample values
    :param values: list, list of sample values
    :return: float, variance of sample values
    '''
    #use average value of values as the expect value
    expectValue = Average(values)

    sum = 0.0
    for value in values:
        sum += (value-expectValue)**2

    return sum / (len(values)-1)

def StandardDeviation(values):
    '''
    compute standard deviation of sample values
    :param values: list, list of sample values
    :return: float, standard deviation of sample values
    '''
    return math.sqrt(Variance(values))

def Covariance(valuesA, valuesB):
    '''
    compute the covariance of sample valuesA and valuesB
    :param valuesA: list, list of sample values A
    :param valuesB: list, list of sample values B
    :return: float, covariance of sample values A and B
    '''
    if len(valuesA) != len(valuesB):
        raise Exception("length of values A and B is not equal!")

    expectValueA = Average(valuesA)
    expectValueB = Average(valuesB)

    sum = 0.0
    idx = num = len(valuesA)
    while idx > 0:
        idx -= 1
        sum += (valuesA[idx]-expectValueA)*(valuesB[idx]-expectValueB)

    return sum / (num-1)

def Correlation(valuesA, valuesB):
    '''
    compute the correlation of sample valuesA and valuesB, using pearson correlation algorithm
    :param valuesA: list, list of sample values A
    :param valuesB: list, list of sample values B
    :return:
    '''
    if len(valuesA) != len(valuesB):
        raise Exception("length of values A and B is not equal!")
    #compute covariance of valuesA and valuesB
    covarianceAB = Covariance(valuesA, valuesB)

    #compute the standard deviation of valuesA, valuesB
    standardDeviationA = StandardDeviation(valuesA)
    standardDeviationB = StandardDeviation(valuesB)

    return covarianceAB/(standardDeviationA*standardDeviationB)