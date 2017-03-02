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

def LeftShiftSub(array, subfunc = None, arg = None, start = 1, end = -1):
    '''
    left shift subtract of the array from @start to @end, algorithm:
        result[i] = array[i] - array[i-1]
    constraint:
        i > 1 and end <len(array)
    :param array: list, array to be left shift sub
    :param subfunc: funciton, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :param start: int, start pos to be sub, must be larger than 0
    :param end: int, end pos to be sub, -1 means last pos, must be larger than start
    :return:list, sub result
    '''
    end = len(array)-1 if end == -1 else end

    if start < 1 or start >= len(array):
        raise Exception("start pos is invalid, must be large than 0 and less than len(array)!")

    if end >= len(array) or (end != -1 and end < start):
        raise Exception("end pos is invalid!, must be less than len(array) and larger than start")

    result = []
    for i in range(start, end+1):
        if(subfunc is None) :
            result.append(array[i] - array[i-1])
        else:
            result.append(subfunc(array[i], array[i-1], arg))

    return result


def RightShiftSub(array, subfunc = None, arg = None, start = 0, end = -1):
    '''
    right shift subtract of the array from @start to @end, algorithm:
        result[i] = array[i] - array[i-1]
    constraint:
        i > 1 and end <len(array)
    :param array: list, array to be right shift sub
    :param subfunc: funciton, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :param start: int, start pos to be sub, must be larger than 0
    :param end: int, end pos to be sub, -1 means last pos, must be larger than start
    :return:list, sub result
    '''
    end = len(array)-1 if end == -1 else end

    if start < 0 or start >= len(array):
        raise Exception("start pos is invalid, must be large than 0 and less than len(array)!")

    if end >= len(array) or (end != -1 and end < start):
        raise Exception("end pos is invalid!, must be less than len(array) and larger than start")

    result = []
    for i in Reverse(range(start+1, end+1)):
        if(subfunc is None) :
            result.append(array[i-1] - array[i])
        else:
            result.append(subfunc(array[i-1], array[i], arg))

    return result