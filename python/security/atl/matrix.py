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


if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9,10]
    print(tomatrix(arr, 2, 5, 1))
