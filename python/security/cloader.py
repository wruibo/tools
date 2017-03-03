'''
    load data from different resources
'''

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