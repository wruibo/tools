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
import atl

from .array import Array


def create(*args):
    """
        create a matrix object
    :param args:
    :return:
    """
    return Matrix(*args)


def matrix(arr, *dims):
    """
        array to matrix
    :param array:
    :param dims:
    :return:
    """
    if len(arr) % atl.math.product(dims) != 0:
        raise Exception("create matrix from array need satisfied dimensions.")

    if len(dims) == 1:
        return arr

    # matrix array
    mtx = Matrix()

    spltcnt, cnt = dims[0], int(len(arr)/dims[0])
    for i in range(0, spltcnt):
        s, e = i*cnt, (i+1)*cnt
        mtx.append(matrix(arr[s:e], *dims[1:]))

    return mtx


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


def reshape(mtx, *dims):
    """
        reshape the input matrix
    :param ma:
    :param dims:
    :return:
    """
    if atl.math.product(dimension(mtx)) != atl.math.product(dims):
        raise Exception("reshaped matrix must have the same elements with source matrix.")

    from . import array
    return matrix(array.array(mtx), *dims)


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


class Matrix(list):
    """
        matrix class
    """
    def __init__(self, *args):
        super(Matrix, self).__init__(*args)

    def dimension(self):
        return dimension(self)

    def reshape(self, *dims):
        self = Matrix(reshape(self, *dims))
        return self

    def numrows(self):
        return numrows(self)

    def numcols(self):
        return numcols(self)

    def subrows(self, *nums):
        return Matrix(subrows(self, *nums))

    def subrow(self, num):
        return Array(subrow(self, num))

    def subcols(self, *nums):
        return Matrix(subcols(self, *nums))

    def subcol(self, num):
        return Array(subcol(self, num))

    def submtx(self, rows=None, cols=None):
        return Matrix(submtx(self, rows, cols))

    def hflip(self):
        return Matrix(hflip(self))

    def vflip(self):
        return Matrix(vflip(self))

    def transpose(self):
        return Matrix(transpose(self))

    def msort(self, oncol, asc=True):
        return Matrix(msort(self, oncol, asc))

    def join(self, withmtx, oncol, withcol):
        return Matrix(join(self, withmtx, oncol, withcol))

    def split(self, bycls, oncol):
        return split(self, bycls, oncol)

if __name__ == "__main__":
    mtx1 = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    mtx2 = [[1, 9, 4], [3, 7, 8]]

    print(hflip(mtx1))
    print(mtx1)
