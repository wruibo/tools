'''
    useful matrix data process functions
'''
import carray

def CreateByColumnNumber(columnNumber):
    '''
    create a empty matrix by specified column number
    :param columnNumber: int, column number of the matrix
    :return: list of list, empty matrix:
        [
            [], [], [], ... # total empty list with column number
        ]
    '''
    matrix = []
    for i in range(0, columnNumber):
        matrix.append([])

    return matrix

def Transpose(matrix):
    '''
    transpose input matrix
    :param list: 2 dimension list, matrix to be transposed
    :return: list, 2 dimension list, result of transpose
    '''
    rows, columns = len(matrix), len(matrix[0])
    transposedMatrix = CreateByColumnNumber(columns)

    for i in range(0, rows):
        for j in range(0, columns):
            transposedMatrix[j].append(matrix[i][j])


    return transposedMatrix

def ExtractRow(matrix, row):
    '''
    extract specified row from matirx
    :param mmatrix: list, matrix using list of list structure
    :param row: int, specified row to extract, index start from 1
    :return: list, row extracted
    '''

    return matrix[row-1]

def ExtractRows(matrix, rows):
    '''
    extract specified rows from matrix
    :param matrix: list, matrix using list of list structure
    :param rows: list, specified rows to extract, [row1, row2, ...], index start from 1
    :return: list, rows extracted, store in list of list, [[rows], [rows],[rows]]
    '''
    extractedRows = []
    for rowIdx in rows:
        extractedRows.append(matrix[rowIdx - 1])

    return extractedRows

def ExtractColumn(matrix, column):
    '''
    extract specified column from matrix
    :param matrix: list, matrix using list of list structure
    :param column: int, specified column to extract, , index start from 1
    :return: list, column values extracted
    '''
    extractedColumn = []
    for row in matrix:
        extractedColumn.append(row[column-1])

    return extractedColumn

def ExtractColumns(matrix, columns):
    '''
    extract specified columns from matrix
    :param matrix: list, 2 dimension list
    :param columns: list, specified columns to extract, [column1, column2, ...], , index start from 1
    :return: list, columns extracted, list in list
    '''
    extractedColumns = CreateByColumnNumber(len(columns))

    for row in matrix:
        for i in range(0, len(columns)):
            extractedColumns[i].append(row[columns[i]-1])

    return extractedColumns

def AverageOfRow(matrix, row):
    '''
    compute average value of specified row in the matrix
    :param matrix: list, 2 dimension list
    :param row: int, which row's average to be compute, start from 1
    :return: float, average of specified row
    '''
    sum = 0.0
    for val in matrix[row-1]:
        sum = sum + val
    return sum / len(matrix[0])

def AverageOfRows(matrix, rows):
    '''
    compute average value of specified rows in the matrix
    :param matrix: list, 2 dimension list
    :param row: list, int in list, which rows's average to be compute, start from 1
    :return: list, float in list, average of specified rows in sequence
    '''
    result = []
    for i in range(0, len(rows)):
        result.append(0.0)
        for val in matrix[rows[i]-1]:
            result[i] = result[i] + val

        result[i] = result[i] / len(matrix[0])

    return result

def AverageOfColumn(matrix, column):
    '''
    compute average value of specified column in the matrix
    :param matrix: 2 dimension list
    :param column: int, which column's average to be compute, start from 1
    :return: float, average of specified column
    '''
    sum = 0.0
    for row in matrix:
        sum = sum + row[column-1]
    return sum / len(matrix)

def AverageOfColumns(matrix, columns):
    '''
    compute average values of specified columns in the matrix
    :param matrix: 2 dimension list
    :param columns: list, int in list, which columns's average to be compute, start from 1
    :return: list, float in list, average of specified columns in sequence
    '''
    result = []
    for j in range(0, len(columns)):
        result.append(0.0)

    for i in range(0, len(matrix)):
        for j in range(0, len(columns)):
            result[j] = result[j] + matrix[i][columns[j]-1]

    for i in range(0, len(result)):
        result[i] = result[i] / len(matrix)

    return result

def SubOnRow(matrix, row, subValue, subfunc = None, arg = None):
    '''
    subtract all items in @row of the @matrix with @subvalue
    :param matrix: list, list of list, matrix which row in it to be left shift sub
    :param row: int, row number to subtract, start from 1
    :param subValue: object, type is same as item in the @matrix
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    row = ExtractRow(matrix, row)
    return array.Sub(row, subValue, subfunc, arg)

def SubOnColumn(matrix, column, subValue, subfunc = None, arg = None):
    '''
    subtract all items in @column of the @matrix with @subvalue
    :param matrix: list, list of list, matrix which row in it to be left shift sub
    :param column: int, column number to subtract, start from 1
    :param subValue: object, type is same as item in the @matrix
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    column = ExtractColumn(matrix, column)
    return array.Sub(column, subValue, subfunc, arg)

def LeftShiftSubOnRow(matrix, row, leftValue = None, subfunc = None, arg = None):
    '''
    left shift subtract of the matrix in specific row from @start to @end, algorithm:
        result[i] = matrix[row][i] - matrix[row][i-1]
    :param matrix: list, list of list, matrix which row in it to be left shift sub
    :param row: int, row number to subtract, start from 1
    :param leftValue: object, type is same as item in the @matrix, the first item's subtractor
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    row = ExtractRow(matrix, row)
    return carray.LeftShiftSub(row, leftValue, subfunc, arg)

def LeftShiftSubOnColumn(matrix, column, leftValue = None, subfunc = None, arg = None):
    '''
    left shift subtract of the matrix in specific column from @start to @end, algorithm:
        result[i] = matrix[i][column] - matrix[i][column]
    :param matrix: list, list of list, matrix which row in it to be left shift sub
    :param column: int, column number to subtract, start from 1
    :param leftValue: object, type is same as item in the @matrix, the first item's subtractor
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    column = ExtractColumn(matrix, column)
    return carray.LeftShiftSub(column, leftValue, subfunc, arg)

def RightShiftSubOnRow(matrix, row, rightValue = None, subfunc = None, arg = None):
    '''
    right shift subtract of the matrix in specific row from @start to @end, algorithm:
        result[i] = matrix[row][i] - matrix[row][i-1]

    :param matrix: list, list of list, matrix which row in it to be right shift sub
    :param row: int, row number to subtract, start from 1
    :param rightValue: object, type is same as item in the @matrix, the last item's subtractor
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    row = ExtractRow(matrix, row)
    return carray.RightShiftSub(row, rightValue, subfunc, arg)

def RightShiftSubOnColumn(matrix, column, rightValue = None, subfunc = None, arg = None):
    '''
    right shift subtract of the matrix in specific column from @start to @end, algorithm:
        result[i] = matrix[i][column] - matrix[i][column]
    :param matrix: list, list of list, matrix which row in it to be left shift sub
    :param column: int, column number to subtract, start from 1
    :param rightValue: object, type is same as item in the @matrix, the last item's subtractor
    :param subfunc: function, self definition for subtract operation, subfunc(a, b, arg)
    :param arg: object, argument passed to subfunc(a, b, arg)
    :return:list, sub result
    '''
    column = ExtractColumn(matrix, column)
    return carray.RightShiftSub(column, rightValue, subfunc, arg)