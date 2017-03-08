'''
    load data from different resources
'''
import cutil

def FileLoadAll(strFilePath, strColumnDelimiter = None, nSkipRows = 0):
    '''
    load data into matrix from the input file with all columns, use the specified column separator, and
    return the load result as a matrix(2 dimension list)
    :param strFilePath: string, file path to be load
    :param strColumnDelimiter: string, column delimiter, default ","
    :return: matrix, 2 dimension list, row list with column string values which is also a list
    example:
        [
            [column11, column12, column13, ...]
            [column21, column22, column23, ...]
            [column31, column32, column33, ...]
            ...
        ]
    '''
    matrix = []
    for row in open(strFilePath):
        if nSkipRows > 0:
            nSkipRows = nSkipRows - 1
            continue

        row = row.split(strColumnDelimiter)
        for i in range(0, len(row)):
            row[i] = row[i].strip()

        matrix.append(row)

    return matrix

def FileLoadColumns(strFilePath, strColumns, strColumnDelimiter = None, nSkipRows = 0):
    '''
    load data into matrix from the input file @strFilePath with specified @strColumns , which column separated by
    @stringColumnSeparator
    :param strFilePath: string, file path to be load
    :param strColumns: string, specify the column with "," separated, format like "col1,col2,...", None means all columns
    :param strColumnDelimiter: string, column delimiter, default ","
    :return: matrix, 2 dimension list, row list with column string values which is also a list
    example:
    [
        [column11, column12, column13, ...]
        [column21, column22, column23, ...]
        [column31, column32, column33, ...]
        ...
    ]
    '''
    columns = cutil.ConvertType(strColumns.split(","), int)
    if len(columns) == 0:
        raise Exception("column specified to load from file is not valid!")

    matrix = []
    for row in open(strFilePath):
        if nSkipRows > 0:
            nSkipRows = nSkipRows - 1
            continue

        newRow = []

        row = row.split(strColumnDelimiter)
        for i in range(0, len(columns)):
            newRow.append(row[columns[i]-1].strip())

        matrix.append(newRow)

    return matrix
