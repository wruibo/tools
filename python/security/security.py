import sys

def SlowDrawdown(values):
    '''
    compute the drawdown of the given values, using normal algorithm:
        values = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param values: list, with element number
    :return: [drawdown, position i, value i, position j, value j] of the list values
    '''
    pMax, vMax, pMin, vMin, drawdown = None, None, None, None, None

    i = j = 0
    while i < len(values):
        j = i + 1
        while j < len(values):
            ijDrawdown = (values[j] - values[i]) / values[i]
            if (drawdown is None and ijDrawdown<0.0) or ijDrawdown < drawdown:
                pMax, vMax, pMin, vMin, drawdown = i, values[i], j, values[j], ijDrawdown
            j = j + 1
        i = i + 1

    return drawdown, pMax, vMax, pMin, vMin


def FastDrawdown(values):
    '''
    compute the drawdown of the given values, using fast algorithm:
        values = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param values: list, with element number
    :return: [drawdown, position i, value i, position j, value j] of the list values
    '''
    pMax, vMax, pMin, vMin, drawdown = None, None, None, None, None
    iPos, iValue, jPos, jValue, ijDrawdown = None, None, None, None, None

    i = j = 0
    while i + 1 < len(values) and j + 1 < len(values):
        if values[i] < values[i+1]:
            i = i + 1
            continue
        j = i + 1
        while j + 1 < len(values):
            if values[j] < values[j-1] and values[j] < values[j+1]:
                if ijDrawdown is None or values[j] < jValue:
                    iPos, iValue, jPos, jValue, ijDrawdown = i, values[i], j, values[j], (values[j] - values[i]) / values[i]

                if drawdown is None or ijDrawdown < drawdown:
                    pMax, vMax, pMin, vMin, drawdown = iPos, iValue, jPos, jValue, ijDrawdown
            else:
                if values[j] > values[i]:
                    i = j
                    iPos, iValue, jPos, jValue, ijDrawdown = None, None, None, None, None
                    break
            j = j + 1

    if i < j < len(values):
        if ijDrawdown is None or values[j] < jValue:
            iPos, iValue, jPos, jValue, ijDrawdown = i, values[i], j, values[j], (values[j] - values[i]) / values[i]

        if drawdown is None or ijDrawdown < drawdown:
            pMax, vMax, pMin, vMin, drawdown = iPos, iValue, jPos, jValue, ijDrawdown

    return drawdown, pMax, vMax, pMin, vMin

def Drawdown(values):
    '''
    compute the drawdown of the given values, using fast algorithm:
        values = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param values: list, with element number
    :return: [drawdown, position i, value i, position j, value j] of the list values
    '''
    return FastDrawdown(values)

if __name__ == "__main__":
    #values = [0.9123, 0.9223, 0.9323]
    #values = [1.202, 0.712, 0.612]
    #values = [1.202]
    #values = [1.202, 0.712, 0.612, 0.77, 0.6]
    #values = [0.9123, 0.9223, 0.9323, 0.8123, 0.8023, 0.8123, 0.8231, 1.021, 1.026, 1.102, 1.202, 0.712, 0.612, 0.77, 0.6]
    values = []
    for value in open("netvalues"):
        values.append(float(value.strip()))

    values.reverse()
    print SlowDrawdown(values)
    print FastDrawdown(values)