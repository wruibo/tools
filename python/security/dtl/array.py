"""
    array for data process
"""
'''
    useful array data process functions
'''

def Create(size, value):
    '''
    create array with @size, use @value initialize every item in the array
    :param size: int, size of the array
    :param value: object, value to initialize the array items
    :return: list, array created
    '''
    array = []
    for i in range(0, size):
        array.append(value)

    return array

def Reverse(array):
    '''
    reverse array elements
    :param array: list, array to be reverse
    :return: list, reverse result
    '''
    result = []
    for i in range(0, len(array)):
        result.append(array[-i-1])

    return result

def Average(array):
    '''
    compute the average of values in the array
    :param array: list, 1 dimension array
    :return: float, average of values in the array
    '''
    sum = 0.0
    for val in array:
        sum = sum + val

    return sum / len(array)

def Sub(array, subValue, subFunc = None, arg = None):
    '''
    subtract all item in @array with @subValue
    :param array: list, whose item will be subtracted
    :param subValue: object, subtract value
    :param subFunc: function, subtract operator
    :param arg: object, argument pass to the @subFunc
    :return: list, array subtracted by the @subValue
    '''
    result = []
    if subFunc is None:
        for value in array:
            result.append(value - subValue)
    else:
        for value in array:
            result.append(subFunc(value, subValue, arg))

    return result

def Multi(array, multiValue, multiFunc = None, arg = None):
    '''
    multiply all item in @array with @multiValue
    :param array: list, whose item will be multiplied
    :param multiValue: object, multi value
    :param multiFunc: function, multi operator
    :param arg: object, argument pass to the @multiFunc
    :return: list, array multiplied by the @multiValue
    '''
    result = []
    if multiFunc is None:
        for value in array:
            result.append(float(value) * float(multiValue))
    else:
        for value in array:
            result.append(multiFunc(value, multiValue, arg))

    return result

def Div(array, divValue, divFunc = None, arg = None):
    '''
    divide all item in @array with @divValue
    :param array: list, whose item will be divided
    :param divValue: object, division value
    :param divFunc: function, division operator
    :param arg: object, argument pass to the @divFunc
    :return: list, array divided by the @divValue
    '''
    result = []

    if divFunc is None:
        for value in array:
            result.append(float(value) / float(divValue))
    else:
        for value in array:
            result.append(divFunc(value, divValue, arg))

    return result

def DivArray(array, divisionArray, divFunc = None, arg = None):
    '''
    divide item in @array by @divisionArray one-correspond-one with sampe index
    :param array: list, array to be divided
    :param divisionArray: list, division array
    :param divFunc: function, division operator
    :param arg: object, argument pass to the @divFunc
    :return:
    '''

    result = []

    if divFunc is None:
        for i in range(0, len(array)):
            result.append(float(array[i]) / float(divisionArray[i]))
    else:
        for i in range(0, len(array)):
            result.append(divFunc(array[i], divisionArray[i], arg))

    return result

def CycleGrowthRate(array, baseValue = None):
    '''
    compute the cycle growth rate of @array
    :param array: list, number value in list
    :param baseValue: number, growth compare base for the first value in @array
    :return: list, float in array
    '''
    if baseValue is None:
        baseValue = array[0]

    result = []
    result.append((float(array[0]) - float(baseValue))/float(baseValue))

    for i in range(1, len(array)):
        result.append((float(array[i]) - float(array[i-1]))/ float(array[i-1]))

    return result

def CompareGrowthRate(array, compareArray):
    '''
    compare the growth with array and compareArray
    :param array: list, number value in list
    :param compareArray: list, number in list
    :return: list, compare growth to @compareArray
    '''
    result = []

    for i in range(0, len(array)):
        result.append((float(array[i]) - float(compareArray[i]))/float(compareArray[i]))

    return result

def LeftShiftSub(array, leftValue = None, subFunc = None, arg = None):
    '''
    left shift subtract of the array from @start to @end, algorithm:
        result[i] = array[i] - array[i-1]
    :param array: list, array to be left shift sub
    :param leftValue: object, type is same as item in the @array, the first item's subtractor
    :param subFunc: function, self definition for subtract operation, subFunc(a, b, arg)
    :param arg: object, argument passed to subFunc(a, b, arg)
    :return:list, sub result
    '''
    result = []

    if subFunc is None:
        if leftValue is None:
            result.append(type(array[0])(0))
        else:
            result.append(array[0] - leftValue)

        for i in range(1, len(array)):
            result.append(array[i] - array[i - 1])
    else:
        if leftValue is None:
            result.append(type(array[0])(0))
        else:
            result.append(subFunc(array[0], leftValue, arg))

        for i in range(1, len(array)):
            result.append(subFunc(array[i], array[i - 1], arg))

    return result


def RightShiftSub(array, rightValue = None, subFunc = None, arg = None):
    '''
    right shift subtract of the array from @start to @end, algorithm:
        result[i] = array[i] - array[i-1]
    constraint:
        i > 1 and end <len(array)
    :param array: list, array to be right shift sub
    :param rightValue: object, type is same as item in the @array, the last item's subtractor
    :param subFunc: funciton, self definition for subtract operation, subFunc(a, b, arg)
    :param arg: object, argument passed to subFunc(a, b, arg)
    :return:list, sub result
    '''
    result = []

    if subFunc is None:
        if rightValue is None:
            result.append(type(array[0])(0))
        else:
            result.append(array[-1] - rightValue)

        for i in Reverse(range(1, len(array))):
            result.append(array[i-1] - array[i])
    else:
        if rightValue is None:
            result.append(type(array[0])(0))
        else:
            result.append(subFunc(array[-1], rightValue, arg))

        for i in Reverse(range(1, len(array))):
            result.append(subFunc(array[i-1], array[i], arg))

    return result
