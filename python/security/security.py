import sys, math, datetime

def Average(values):
    '''
    compute average of sample values
    :param values: list of sample values
    :return: float, average of sample values
    '''
    return sum(values) / len(values)

def Variance(values):
    '''
    compute variance of sample values
    :param values: list of sample values
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
    :param values: list of sample values
    :return: float, standard deviation of sample values
    '''
    return math.sqrt(Variance(values))

def Covariance(valuesA, valuesB):
    '''
    compute the covariance of sample valuesA and valuesB
    :param valuesA: list of sample values A
    :param valuesB: list of sample values B
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
    :param valuesA:
    :param valuesB:
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

def SlowMaxDrawdown(values):
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


def FastMaxDrawdown(values):
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

def MaxDrawdown(values):
    '''
    compute the drawdown of the given values, using fast algorithm:
        values = {v1, v2, ... , vn}
        drawdown = max{vi-vj/vi}, i<j<=n
    :param values: list, with element number
    :return: [drawdown, position i, value i, position j, value j] of the list values
    '''
    return FastMaxDrawdown(values)

def __DaysBetween(strStartDate, strEndDate, strFormat):
    '''
    compute the days between start date and end date
    :param strStartDate: string, start date sting with @strFormat
    :param strEndDate: string, end date string with @strFormat
    :param strFormat: string, format of the input start and end date string
    :return: number, days between start date and end date
    '''
    return (datetime.datetime.strptime(strStartDate, strFormat) - datetime.datetime.strptime(strStartDate, strFormat)).days

def __ExtractRowFromMatrix(matrix, row):
    '''
    extract specified row from matirx
    :param mmatrix: list, matrix using list of list structure
    :param row: int, specified row to extract
    :return: list, row extracted
    '''

    return matrix[row-1]

def __ExtractRowsFromMatrix(matrix, rows):
    '''
    extract specified row from matrix
    :param matrix: list, matrix using list of list structure
    :param rows: list, specified rows to extract, [row1, row2, ...]
    :return: list, rows extracted, store in list of list, [[rows], [rows],[rows]]
    '''
    extractedRows = []
    for rowIdx in rows:
        rowIdx = rowIdx - 1
        extractedRows.append(matrix[rowIdx])

    return extractedRows

def __ExtractColumnFromMatrix(matrix, column):
    '''
    extract specified column from matrix
    :param matrix: list, matrix using list of list structure
    :param column: int, specified column to extract
    :return: list, column values extracted
    '''
    extractedColumn = []
    for row in matrix:
        extractedColumn.append(row[column-1])

    return extractedColumn

def __ExtractColumnsFromMatrix(matrix, columns):
    '''
    extract specified columns from matrix
    :param matrix: list, matrix using list of list structure
    :param columns: list, specifed columns to extract, int list
    :return: list, columns extracted, list in list
    '''
    extractedColumns = []
    for i in range(0, len(columns)):
        extractedColumns.append([])

    for row in matrix:
        idx = 0
        for columnIdx in columns:
            extractedColumns[idx].append(row[columnIdx-1])
            idx = idx + 1

    return extractedColumns

def __SequenceOfYearRevenuesFromSequenceOfDatePrices(sequenceOfDatePrices, columns = None, strDateFormat = "%Y%m%d"):
    '''
    compute year revenue sequence from the date price sequence
    :param sequenceOfDatePrices: list,
        sequence of date price, example:
        [
            [date, price of assets A, price of assets B, ...],
            [date, price of assets A, price of assets B, ...],
            ...
        ]

        date: string, format specified by @strDateFormat
    :param columns: list, specified assets column, int list, start from 2
    :param strDateFormat: string, date format string if use the sequence of date price value
    :return: list of list, matrix, column is assets number, row is assets interval revenue
        [
            [year revenue of assets A, year revenue of assets B, ...]
            [year revenue of assets A, year revenue of assets B, ...]
            [year revenue of assets A, year revenue of assets B, ...]
            ...
        ]
    '''
    #initialize the columns
    if columns is None:
        columns = range(1, len(sequenceOfDatePrices[0]))

    #initialize the sequence of year revenue list
    sequenceOfYearRevenues = []
    for i in range(0, len(columns)):
        sequenceOfYearRevenues.append([])

    #compute sequence of year revenue for each assets
    for i in range(1, len(sequenceOfDatePrices)):
        days = __DaysBetween(sequenceOfDatePrices[i-1][0], sequenceOfDatePrices[i][0], strDateFormat)

        for j in range(0, len(columns)):
            revenue = (float(sequenceOfDatePrices[i][columns[j]-1]) - float(sequenceOfDatePrices[i-1][columns[j]-1])) / float(sequenceOfDatePrices[i-1][columns[j]-1])
            sequenceOfYearRevenues[i-1][j] = 365 * revenue / days

    return sequenceOfYearRevenues

def __ExpectYearRevenuesFromSequenceOfYearRevenues(sequenceOfYearRevenues, columns = None):
    '''

    :param sequenceOfYearRevenues: list,
        sequence of year revenues, example:
        [
            [year revenue of assets A, year revenue of assets B, ...],
            [year revenue of assets A, year revenue of assets B, ...],
            ...
        ]
    :param colums: list, specified assets column, int list, start from 1
    :return: list, revenues for assets specified by columns, example:
        [expect year revenue of assets A, expect year revenue of assets B, ...]
    '''
    #initialize columns when it is None
    if columns is None:
        columns = range(1, len(sequenceOfYearRevenues[0])+1)

    #initialize the return expect year revenues
    expectYearRevenues = []
    for i in range(0, len(columns)):
        expectYearRevenues.append(0.0)

    #compute specified year revenue of assets
    for i in range(0, len(sequenceOfYearRevenues)):
        for j in range(0, len(columns)):
            expectYearRevenues[j] = expectYearRevenues[j] + float(sequenceOfYearRevenues[columns[j]-1])

    for i in range(0, len(expectYearRevenues)):
        expectYearRevenues[i] = expectYearRevenues[i] / len(sequenceOfYearRevenues)

    return expectYearRevenues;

def __ExpectYearRevenuesFromSequenceOfDatePrices(sequenceOfDatePrices, columns = None, strDateFormat = "%Y%m%d"):
    '''

    :param sequenceOfDatePrices: list,
        sequence of date price, example:
        [
            [date, price of assets A, price of assets B, ...],
            [date, price of assets A, price of assets B, ...],
            ...
        ]

        date: string, format specified by @strDateFormat
    :param columns: list, specified assets column, int list, start from 2
    :param strDateFormat: string, date format string if use the sequence of date price value
    :return:list, revenues for assets specified by columns, example:
        [expect year revenue of assets A, expect year revenue of assets B, ...]
    '''
    #compute the revenue matrix of specified assets
    sequenceOfYearRevenues = __SequenceOfYearRevenuesFromSequenceOfDatePrices(sequenceOfDatePrices, columns, strDateFormat)

    return __ExpectYearRevenuesFromSequenceOfYearRevenues(sequenceOfYearRevenues)

def __SharpeRatioWithSequenceOfYearRevenue(sequenceOfYearRevenue, rf):
    '''
    compute sharpe ratio with the input list of sample year revenues
    :param sequenceOfYearRevenue: list with float element, sample sequence of year revenue
    :param rf: risk free market year revenue ratio
    :return: sharpe ratio of the give sample data
    '''
    # use the average of values as the expect value
    expectRevenue = Average(sequenceOfYearRevenue)

    standardDeviation = StandardDeviation(sequenceOfYearRevenue)

    return (expectRevenue - rf) / standardDeviation

def __SharpeRatioWithSequenceOfDateNetValue(sequenceOfDateNetValue, rf):
    '''
    compute the sharpe ratio with the input list of sample net values
    :param sequenceOfDateNetValue: list with sequence of date net value [date(YYYYmmdd), net-value] elements
    :param rf: risk free market year revenue ratio
    :return: sharpe ratio of the give sample data
    '''
    #compute the sequence of year revenue according to the sequence of the date net values
    sequenceOfYearRevenue = []
    idx = 1;
    while idx < len(sequenceOfDateNetValue):
        days = __DaysBetween(sequenceOfDateNetValue[idx-1][0], sequenceOfDateNetValue[idx][0])
        revenue = sequenceOfDateNetValue[idx][1] - sequenceOfDateNetValue[idx-1][1]
        sequenceOfYearRevenue[idx-1] = 365 * revenue / days * sequenceOfDateNetValue[idx-1][1];
        idx = idx + 1

    return __SharpeRatioWithSequenceOfYearRevenue(sequenceOfYearRevenue, rf)

def SharpeRatio(sequenceOfDateNetValueOrYearRevenue, rf, strDateFormat = "%Y%m%d"):
    '''
    compute sharpe ratio of the given values
    :param sequenceOfDateNetValueOrYearRevenue: list,
        sequence of date net value[[date string, net-value], [date string, net-value], ...],
        or
        year revenue value[revenue1, revenue2, ...]
    :param rf: float, risk free market year revenue ratio
    :param strDateFormat: string, date format string if use the sequence of date net value
    :return: float, sharpe ratio of the give sample data
    '''
    if isinstance(sequenceOfDateNetValueOrYearRevenue, list) and isinstance(sequenceOfDateNetValueOrYearRevenue[0], list) :
        return __SharpeRatioWithSequenceOfDateNetValue(sequenceOfDateNetValueOrYearRevenue, rf, strDateFormat)
    else:
        return __SharpeRatioWithSequenceOfYearRevenue(sequenceOfDateNetValueOrYearRevenue, rf)


def __BetaFactorWithSequenceOfYearRevenue(sequenceOfYearRevenue):
    '''
    compute beta factor of fund, using the fund's and market's sample year revenue
    :param sequenceOfYearRevenue: list,
        list of fund's and market's sample year revenue, example:
        [
            [fund-year-revenue1, market-year-revenue1],
            [fund-year-revenue2, market-year-revenue2],
            .
            .
            .
        ]
    :return: float, beta factor of fund
    '''
    #extract fund's and market's year revenue sequence
    sequenceOfFundYearRevenue = sequenceOfMarketYearRevenue = []
    for item in sequenceOfYearRevenue:
        sequenceOfFundYearRevenue.append(item[0])
        sequenceOfMarketYearRevenue.append(item[1])

    #compute the covariance of fund's and market's sample year revenue
    covarianceFundWithMarket = Covariance(sequenceOfFundYearRevenue, sequenceOfMarketYearRevenue)
    varianceOfMarket = Variance(sequenceOfMarketYearRevenue)

    return covarianceFundWithMarket / varianceOfMarket


def __BetaFactorWithSequenceOfDatePrice(sequenceOfDatePrice, strDateFormat):
    '''
    compute the beta factor of fund, using the fund's and market's date sample price value
    :param sequenceOfDatePrice: list, format like this
        [
            [date, fund-net-value, market-index-value],
            [date, fund-net-value, market-index-value],
            [date, fund-net-value, market-index-value],
            ......
        ]
        order by date closely
    :param strDateFormat: string, date string format in the sequence
    :return: float, beta factor of fund
    '''
    #split the fund's and market's date price
    sequenceOfFundDatePrice = sequenceOfMarketDatePrice = []
    for item in sequenceOfDatePrice:
        sequenceOfFundDatePrice.append([item[0], item[1]])
        sequenceOfMarketDatePrice.append([item[0], item[2]])

    #compute the year revenue of fund and market
    sequenceOfFundYearRevenue = YearRevenueFromDatePrice(sequenceOfFundDatePrice)
    sequenceOfMarketYearRevenue = YearRevenueFromDatePrice(sequenceOfMarketDatePrice)

    __SequenceOfYearRevenuesFromSequenceOfDatePrices(sequenceOfDatePrice, [2, 3], strDateFormat)

    # compute the covariance of fund's and market's sample year revenue
    covarianceFundWithMarket = Covariance(sequenceOfFundYearRevenue, sequenceOfMarketYearRevenue)
    varianceOfMarket = Variance(sequenceOfMarketYearRevenue)

    return covarianceFundWithMarket / varianceOfMarket

def BetaFactor(sequenceOfDatePriceOrYearRevenue, strDateFormat = "%Y%m%d"):
    '''
    compute the beta factor of given found, algorithm:
        bp = Cov(Rp, Rm)/Variance(Rm)

    :param sequenceOfDatePriceOrYearRevenue: list, there are 2 format
        format1: sequence with date price of fund's and market's
        [
            [date, fund-net-value, market-index-value],
            [date, fund-net-value, market-index-value],
            ......
        ]
        or
        format2: sequence with year revenue of fund's and market's
        [
            [fund-year-revenue, market-year-revenue],
            [fund-year-revenue, market-year-revenue],
            ......
        ]
    :param strDateFormat: string, date string format if using date price sequence
    :return: float, beta factor of fund
    '''
    if isinstance(sequenceOfDatePriceOrYearRevenue, list) and isinstance(sequenceOfDatePriceOrYearRevenue[0], list) and len(sequenceOfDatePriceOrYearRevenue[0]) == 2:
        #input is year revenue sequence
        return __BetaFactorWithSequenceOfYearRevenue(sequenceOfDatePriceOrYearRevenue)
    else:
        #input is date price sequence
        return __BetaFactorWithSequenceOfYearRevenue(sequenceOfDatePriceOrYearRevenue, strDateFormat)


def TreynorRatio(sequenceOfDatePriceOrYearRevenue, rf, strDateFormat = "%Y%m%d"):
    '''
    compute the Treynor ratio of given fund
    :param sequenceOfDatePriceOrYearRevenue:  list, there are 2 format
        format1: sequence with date price of fund's and market's
        [
            [date, fund-net-value, market-index-value],
            [date, fund-net-value, market-index-value],
            ......
        ]
        or
        format2: sequence with year revenue of fund's and market's
        [
            [fund-year-revenue, market-year-revenue],
            [fund-year-revenue, market-year-revenue],
            ......
        ]
    :param rf: float, risk free market year revenue ratio
    :param strDateFormat: string, date string format if using date price sequence
    :return: float, Treynor ration of fund
    '''

    #compute the expect year revenue of fund
    fundExpectYearRevenue = 0.0
    if isinstance(sequenceOfDatePriceOrYearRevenue, list) and isinstance(sequenceOfDatePriceOrYearRevenue[0], list) and len(sequenceOfDatePriceOrYearRevenue[0]) == 2:
        #input is year revenue sequence
        fundExpectYearRevenue, = __ExpectYearRevenuesFromSequenceOfYearRevenues(sequenceOfDatePriceOrYearRevenue, [1])
    else:
        #input is date price sequence
        fundExpectYearRevenue, = __ExpectYearRevenuesFromSequenceOfDatePrices(sequenceOfDatePriceOrYearRevenue, [2], strDateFormat)

    #compute beta factor of fund
    fundBetaFactor = BetaFactor(sequenceOfDatePriceOrYearRevenue, strDateFormat)

    return fundExpectYearRevenue - rf / fundBetaFactor

def JensenRatio(sequenceOfDatePriceOrYearRevenue, rf, strDateFormat = "%Y%m%d"):
    '''
     compute the Jensen ratio of given fund, the Jensen ration also called alpha value of fund, algorithm:
                 Jp = rp - [rf + bp(rm-rf)]
     where
        rp is the expect revenue of fund p,
        rf is the market risk free revenue,
        bp is beta factor of fund p,
        rm is the expect revenue of market m
     :param sequenceOfDatePriceOrYearRevenue:  list, there are 2 format
         format1: sequence with date price of fund's and market's
         [
             [date, fund-net-value, market-index-value],
             [date, fund-net-value, market-index-value],
             ......
         ]
         or
         format2: sequence with year revenue of fund's and market's
         [
             [fund-year-revenue, market-year-revenue],
             [fund-year-revenue, market-year-revenue],
             ......
         ]
     :param rf: float, risk free market year revenue ratio
     :param strDateFormat: string, date string format if using date price sequence
     :return: float, Jensen ration of fund
    '''

    #compute
    rp = rm = 0.0
    if isinstance(sequenceOfDatePriceOrYearRevenue, list) and isinstance(sequenceOfDatePriceOrYearRevenue[0],list) and len(sequenceOfDatePriceOrYearRevenue[0]) == 2:
        # input is year revenue sequence
        rp, rm = __ExpectYearRevenuesFromSequenceOfYearRevenues(sequenceOfDatePriceOrYearRevenue)
    else:
        # input is date price sequence
        rp, rm = __ExpectYearRevenueFromSequenceOfDatePrice(sequenceOfDatePriceOrYearRevenue, [2, 3], strDateFormat)

    #compute beta factor of fund
    bp = BetaFactor(sequenceOfDatePriceOrYearRevenue, strDateFormat)

    return rp - (rf + bp(rm - rf))


def ConvertItemTypeInContainer(container, type):
    '''
    convert the item type in the container to specified type recursively
    :param container: list or Object, whose item will be converted
    :param type: type, type to be convert to
    :return: list or Object, convert result
    '''
    if isinstance(container, list):
        result = []
        for item in container:
            result.append(ConvertItemTypeInContainer(item, type))
        return result
    else:
        return type(container)

def LoadDataWithAllColumns(strFilePath, strColumnSeparator=",", stripBlank = True):
    '''
    load data from the input file with all columns, use the specified column separator, and
    return the load result as a matrix(2 dimension list)
    :param strFilePath: string, file path to be load
    :param strColumnSeparator: string, column separator, default ","
    :param stripBlank: bool, flag for strip the blank character for the collum value
    :return: list, 2 dimension list, row list with column string values which is also a list
    '''
    rows = []
    for strRow in open(strFilePath):
        items = strRow.split(strColumnSeparator)

        idx = 0
        if stripBlank:
            for item in items:
                items[idx] = item.strip()

        rows.append(items)

    return rows

def LoadDataWithSepcifiedColumns(strFilePath, strColumnSeparator=",", specifiedColumns = None, stripBlank = True):
    '''
    load data from the input file with specified columns, use the specified column separator, and
    return the load result as a list when only 1 column specified or matrix(2 dimension list) when
    multi columns specified.
    :param strFilePath: string, file path to be load
    :param strColumnSeparator: string, column separator, default ","
    :param specifiedColumns: string, specify the column with "," separated, format like "col1,col2,...", None means all columns
    :param stripBlank: bool, flag for strip the blank character for the collum value
    :return: list or list of list
    '''

    # load all columns when none column specified
    if specifiedColumns is None:
        return LoadDataWithAllColumns(strFilePath, strColumnSeparator, stripBlank)

    columns = ConvertItemTypeInContainer(specifiedColumns.split(","), int)
    if len(columns) == 0:
        raise Exception("specified column is not valid!")

    if len(columns) == 1:
        #only 1 column specified
        row = []
        columnIdx = columns[0]-1
        for strRow in open(strFilePath):
            items = strRow.split(strColumnSeparator)
            if columnIdx < len(items):
                row.append(items[columnIdx] if not stripBlank else items[columnIdx].strip())
            else:
                row.append("")
        return row
    else:
        #multi columns specified
        rows = []
        for strRow in open(strFilePath):
            items = strRow.split(strColumnSeparator)

            columns = []
            for columnIdx in columns:
                columnIdx = columnIdx - 1

                if columnIdx < len(items):
                    columns.append(items[columnIdx] if not stripBlank else items[columnIdx].strip())
                else:
                    columns.append("")

            rows.append(columns)

        return rows

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
    print SlowMaxDrawdown(values)
    print FastMaxDrawdown(values)

    rates = []
    for rate in open("rates"):
        rates.append(float(rate.strip()))

    print SharpeRatio(rates, rates[0], 0.04)

    data = LoadDataWithSepcifiedColumns("sequenceYearRevenue", ",", "1")

    data = ConvertItemTypeInContainer(data, float)

    print SharpeRatio(data, 0.03)