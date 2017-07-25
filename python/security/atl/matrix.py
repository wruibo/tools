"""
    multi-dimension array process methods, matrix storage by 2-dimension array like:
         [
            [v11, v12, ..., v1m]
            [v21, v22, ..., v2m]
            [ ...              ]
            [vn1, vn2, ..., vnm]
         ]
    is an n*m dimension array.
"""


def ismatrix(mtx):
    """
        detect if input @mtx is a matrix
    :param mtx: matrix to be detected
    :return: boolean
    """
    if not (isinstance(mtx, list) or isinstance(mtx, tuple)):
        return False

    len_of_last_row = None
    for row in mtx:
        if not(isinstance(row, list) or isinstance(mtx, tuple)):
            return False

        if len_of_last_row is None:
            len_of_last_row = len(row)
        else:
            if len_of_last_row != len(row):
                return False
            len_of_last_row = len(row)

    return True


def dimension(mtx):
    """
        get dimension of input matrix
    :param mtx: matrix
    :return: tuple, (rows, columns)
    """
    dims = []
    if isinstance(mtx, list) or isinstance(mtx, tuple):
        dims.append(len(mtx))
        leftdims = dimension(mtx[0])
        if len(leftdims) > 0:
            dims.extend(leftdims)

    return dims

def numrows(mtx):
    """
        get the number of rows in matrix
    :param mtx: matrix
    :return: int, number of rows in matrix
    """
    return dimension(mtx)[0]

def numcols(mtx):
    """
        get the number of columns in matrix
    :param mtx: matrix
    :return: int, number of columns in matrix
    """
    return dimension(mtx)[1]


def elements(mtx):
    """
        get all elements from matrix sequentially
    :param mtx: matrix
    :return: array, all elements in array
    """
    if isinstance(mtx, list) or isinstance(mtx, tuple):
        elmts = []
        for elmt in mtx:
            nextelmts = elements(elmt)
            if isinstance(nextelmts, list) or isinstance(nextelmts, tuple):
                elmts.extend(nextelmts)
            else:
                elmts.append(nextelmts)
        return elmts
    else:
        return mtx


def toarray(mtx):
    """
        expend matrix elements to array
    :param mtx: matrix
    :return: list, list with matrix elements
    """
    return elements(mtx)


def tomatrix(arr, *dims):
    """
        array to matrix
    :param array:
    :param dims:
    :return:
    """
    from atl import array

    if len(arr) % array.multi(dims) != 0:
        raise "expend array to matrix need satisfied dimensions."

    if len(dims) == 1:
        return arr

    mtx = []
    spltcnt, cnt = dims[0], int(len(arr)/dims[0])
    for i in range(0, spltcnt):
        s, e = i*cnt, (i+1)*cnt
        mtx.append(tomatrix(arr[s:e], *dims[1:]))
    return mtx


def reshape(mtx, *dims):
    """
        reshape the input matrix
    :param ma:
    :param dims:
    :return:
    """
    from atl import array
    if array.multi(dimension(mtx)) != array.multi(dims):
        raise "reshaped matrix must have the same elements with source matrix."

    return tomatrix(toarray(mtx), *dims)


def reverser(mtx):
    """
        reverse matrix on rows, example:
    input:
        [
            [v11, v12, ..., v1m]
            [v21, v22, ..., v2m]
            [ ...              ]
            [vn1, vn2, ..., vnm]
        ]
    output:
        [
            [vn1, vn2, ..., vnm]
            [ ...              ]
            [v21, v22, ..., v2m]
            [v11, v12, ..., v1m]
        ]
    :param mtx: matrix
    :return: matrix, matrix reversed on rows
    """
    if not ismatrix(mtx):
        raise "reversec object must be a matrix"

    newmtx = []

    for i in range(1, len(mtx)+1):
        newmtx.append(mtx[-i].copy())

    return newmtx


def reversec(mtx):
    """
        reverse matrix on columns, example:
    input:
        [
            [v11, v12, ..., v1m]
            [v21, v22, ..., v2m]
            [ ...              ]
            [vn1, vn2, ..., vnm]
        ]
    output:
        [
            [v1m, ..., v12, v11]
            [v2m, ..., v22, v21]

            [vnm, ..., vn2, vn1]
        ]
    :param mtx: matrix
    :return: matrix, matrix reversed on columns
    """
    if not ismatrix(mtx):
        raise "reversec object must be a matrix"

    newmtx = []

    for i in range(0, len(mtx)):
        row = mtx[i].copy()
        row.reverse()
        newmtx.append(row)

    return newmtx

def transpose(mtx):
    """
        transpose matrix
    input:
        [
            [v11, v12, ..., v1m]
            [v21, v22, ..., v2m]
            [ ...              ]
            [vn1, vn2, ..., vnm]
        ]
    output:
        [
            [v11, v21, ..., vn1]
            [v12, v22, ..., vn2]
            [ ...              ]
            [v1m, v2m, ..., vnm]
        ]
    :param ma: matrix, n*m dimensions
    :return: matrix, m*n dimensions
    """
    if not ismatrix(mtx):
        raise "transpone object must be a matrix"

    newmtx = []
    for i in range(0, len(mtx[0])):
        newrow = []
        for row in mtx:
            newrow.append(row[i])
        newmtx.append(newrow)

    return newmtx


def subrows(mtx, *nums):
    """
       get specified sub rows by number from matrix
    :param mtx: matrix
    :param nums: tuple with int numbers, start from 1
    :return: matrix
    """
    rows = []

    for num in nums:
        rows.append(mtx[num-1])

    return rows


def subrow(mtx, num):
    """
        get specified sub row by number from matrix
    :param mtx: matrix
    :param num: int, row number
    :return: array
    """
    return subrows(mtx, num)[0]


def subcols(mtx, *nums):
    """
        get specified sub columns by number from matrix
    :param mtx: matrix
    :param nums: tuple with int numbers, start from 1
    :return:  matrix
    """
    cols = []

    for num in nums:
        col = []
        for row in mtx:
            col.append(row[num-1])
        cols.append(col)

    return cols


def subcol(mtx, num):
    """
        get specified sub column by number from atrix
    :param mtx: matrix
    :param num: int, column number
    :return: array
    """
    return subcols(mtx, num)[0]


def submtx(mtx, rows=None, cols=None):
    """
        get sub matrix by specified rows and columns
    :param mtx: matrix
    :param rows: tuple, row numbers want
    :param cols: tuple, column numbers want
    :return: matrix
    """
    if rows is None and cols is None:
        return mtx

    if rows is None:
        return subcols(cols)

    if cols is None:
        return subrows(rows)

    newmtx = []

    for i in range(0, len(rows)):
        row = []
        for j in range(0, len(cols)):
            row.append(mtx[rows[i]-1][cols[j]-1])
        newmtx.append(row)

    return newmtx


def sort(mtx, oncol, asc=True):
    """
        sort matrix on specified column with ascend flag
    :param mtx: matrix
    :param oncol: int, column number sort on
    :param asc: bool, true - sort ascend, false-sort descend
    :return: matrix, sorted matrix
    """
    pass


def join(mtx1, mtx2, col1, col2):
    """
        join matrix1 and matrix2 on matrix1'column1, matrix2'column2
    :param mtx1: matrix, join, default order ascend on col1
    :param mtx2: matrix, to be join, default order acsend on col2
    :param col1: int, column number of mtx1
    :param col2: int, column number of mtx2
    :return: matrix
    """
    # join result
    mtx = []

    # pointer for mtx1 and mtx2
    pos1, pos2 = 0, 0

    while pos1 < len(mtx1) and pos2 < len(mtx2) :
            # current row in mtx1 & mtx2
            joinvalmtx1, rowmtx1 = mtx1[pos1][col1-1], mtx1[pos1]
            joinvalmtx2, rowmtx2 = mtx2[pos2][col2-1], mtx2[pos2]

            if joinvalmtx2 == joinvalmtx1:
                # add both row to result
                mtx.append(rowmtx1 + rowmtx2)
                # increase both pointer
                pos1 += 1
                pos2 += 1

            elif joinvalmtx1 > joinvalmtx2:
                pos2 += 1
            else:
                pos1 += 1

    return mtx


def split(mtx, bycls, oncol):
    """
        split matrix by class on specified column
    :param mtx: matrix
    :param bycls: class, class for split the matrix on column
    :param oncol: int, column number
    :return: dict, class object->sub matrix
    """
    # split result
    result = {}

    # split the matrix
    lastkey = None
    for row in mtx:
        currkey = bycls(row[oncol-1])
        if lastkey is None:
            lastkey = currkey
            result[lastkey] = [row]
        else:
            if currkey == lastkey:
                result[lastkey].append(row)
            else:
                lastkey = currkey
                result[lastkey] = [row]

    return result

if __name__ == "__main__":
    mtx1 = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    mtx2 = [[1, 9, 4], [3, 7, 8]]

    print(reverser(mtx1))
    print(mtx1)
