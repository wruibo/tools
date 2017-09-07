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
from . import array


def create(arr, *dims):
    """
        array to matrix
    :param array:
    :param dims:
    :return:
    """
    if len(arr) % array.product(dims) != 0:
        raise Exception("create matrix from array need satisfied dimensions.")

    if len(dims) == 1:
        return arr

    # matrix array
    mtx = []

    spltcnt, cnt = dims[0], int(len(arr)/dims[0])
    for i in range(0, spltcnt):
        s, e = i*cnt, (i+1)*cnt
        mtx.append(create(arr[s:e], *dims[1:]))

    return mtx


def ismatrix(obj):
    """
        test if input object is an matrix
    :param obj: object
    :return: boolean, True if input object is matrix
    """
    if not array.isarray(obj):
        return False

    dims = dimension(obj)
    if len(dims) == 2 and dims[0] == dims[1]:
      return True

    return False


def like(mtx1, mtx2):
    """
        test if matrix has the same dimensions and same element types
    :param mtx1: matrix
    :param mtx2: matrix
    :return: boolean, True if two matrix is like each other
    """
    if ismatrix(mtx1) and ismatrix(mtx2):
        if dimension(mtx1) == dimension(mtx2):
            return array.like(mtx1, mtx2)
    return False


def equal(mtx1, mtx2):
    """

    :param mtx1:
    :param mtx2:
    :return:
    """
    if ismatrix(mtx1) and ismatrix(mtx2):
        return mtx1 == mtx2
    return False


def similar(mtx1, mtx2):
    """
        test if matrix has the same dimensions
    :param mtx1: matrix
    :param mtx2: matrix
    :return: boolean, True if two matrix is similar with each other
    """
    if ismatrix(mtx1) and ismatrix(mtx2):
        if dimension(mtx1) == dimension(mtx2):
            return True
    return False


def maxval(mtx, useabs=False):
    """
        get the max value in matrix
    :param mtx: matrix
    :param useabs: boolean, use absolute value
    :return: max value
    """
    return array.maxval(mtx, useabs)


def add(mtx, withval):
    """
        add matrix data with specified value or another matrix
    :param mtx: matrix, which will add with @withval
    :param withval: list or value, which will be added with
    :return: matrix
    """
    return array.add(mtx, withval)


def sub(mtx, withval):
    """
        sub matrix data with specified value or another matrix
    :param mtx: matrix, which will subtract @withval
    :param withval: matrix or value, which will be subtracted with
    :return: matrix
    """
    return array.sub(mtx, withval)


def multi(mtx, withval):
    """
        multi matrix data with specified value or another matrix
    :param mtx: matrix, which will multi @withval
    :param withval: matrix or value, which will be multiplied with
    :return: matrix
    """
    return array.multi(mtx, withval)


def divide(mtx, withval):
    """
        divide matrix data with specified value or another matrix
    :param mtx: matrix, which will multi @withval
    :param withval: matrix or value, which will be divided with
    :return: matrix
    """
    return array.divide(mtx, withval)


def sum(mtx):
    """
        compute sum of data in matrix
    :param mtx: matrix
    :return: sum result
    """
    return array.sum(mtx)


def product(mtx):
    """
        compute product of data in array
    :param mtx, matrix
    :return: product result
    """
    return array.product(mtx)


def normalize(mtx, refer=None):
    """
        normalize values in matrix
    :param mtx: matrix
    :param refer: float, reference value for normalize
    :return:
    """
    return array.normalize(mtx, refer)


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


def strip(mtx):
    """
        change the multi-dimension array @mtx to specified dimension, e.g.:
    input:
        [
            [1, 2, 3],
            [4, 5, 6],
            [[7], [8], [9, 10]]
        ]
    output:
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    :param mtx: list, multi dimension array
    :return: list, one dimension array
    """
    return array.strip(mtx)


def reshape(mtx, *dims):
    """
        reshape the input matrix
    :param ma:
    :param dims:
    :return:
    """
    if array.product(dimension(mtx)) != array.product(dims):
        raise Exception("reshaped matrix must have the same elements with source matrix.")

    return create(strip(mtx), *dims)


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

    return transpose(cols)


def subcol(mtx, num):
    """
        get specified sub column by number from atrix
    :param mtx: matrix
    :param num: int, column number
    :return: array
    """
    col = []
    for row in mtx:
        col.append(row[num-1])
    return col

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


def hflip(mtx):
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
    newmtx = []
    for i in range(1, len(mtx)+1):
        newmtx.append(mtx[-i].copy())
    return newmtx


def vflip(mtx):
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
    newmtx = []
    for i in range(0, len(mtx[0])):
        newrow = []
        for row in mtx:
            newrow.append(row[i])
        newmtx.append(newrow)

    return newmtx


def msort(mtx, oncol, asc=True):
    """
        sort matrix on specified column with ascend flag
    :param mtx: matrix
    :param oncol: int, column number sort on
    :param asc: bool, true - sort ascend, false-sort descend
    :return: matrix, sorted matrix
    """
    newmtx = mtx
    newmtx.sort(key=lambda x: x[oncol-1], reverse=not asc)
    return newmtx


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


def select(mtx, cmp, oncol):
    """
        select rows from matrix by compare @cmp method on specified column @oncol
    :param mtx: matrix
    :param cmp: function
    :param oncol: int, column number
    :return: matrix
    """
    resmtx = []
    for row in mtx:
        if cmp(row[oncol-1]):
            resmtx.append(row)
    return resmtx
