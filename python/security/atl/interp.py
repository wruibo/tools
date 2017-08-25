"""
        interpolation algorithms, input matrix structure:
    input:
        [
            [x0, y11, y12, ..., y1m]
            [x1, y21, y22, ..., y2m]
            [       ...        ]
            [xn, yn1, yn2, ..., ynm]
        ]
    output:
        interpolation result, also a matrix like the input
"""
import atl


def linear(mtx, basecol, step, *cols):
    """
        linear interpolation for specified matrix columns on base column with step
    formula:
        y(x) = y0 + (y1-y0)(x-x0)/(x1-x0)

    :param mtx: matrix
    :param basecol: base column for interpolation
    :param step: step of base column for interpolation
    :param cols: columns to interpolate, default all columns will be interpolated
    :return: matrix
    """
    # default interpolate all columns
    if len(cols)==0:
        cols = list(range(1, dtl.matrix.numcols(mtx)+1))

    # interpolation result
    interpmtx = []

    # process all records
    x0, y0 = None, None
    for i in range(0, len(mtx)):
        # start with the first records
        if x0 is None:
            x0, y0s = mtx[i][basecol-1], [mtx[i][j-1] for j in cols]
            interpmtx.append(y0s)
            continue

        # interpolate values between current value with last
        x1, y1s = mtx[i][basecol-1], [mtx[i][j-1] for j in cols]

        # total steps need to interpolate
        x10, steps = x1-x0, int((x1-x0)/step)-1
        for j in range(1, steps+1):
            x= x0+j*step
            ys, xx0 = [], x-x0
            for k in range(0, len(y0s)):
                y = y0s[k] + ((y1s[k]-y0s[k])/x10) * xx0
                ys.append(y)
            interpmtx.append(ys)

        # add current record to result
        interpmtx.append(y1s)

        # rebase the x0, y0s
        x0, y0s = x1, y1s

    return interpmtx


def _indexs(arr, val):
    """
        get all index for value in the array
    :param arr: array
    :param val: value which indexs want
    :return: array
    """
    indexs = []
    for i in range(0, len(arr)):
        if arr[i] == val:
            indexs.append(i)
    return indexs if len(indexs) is not 0 else None


def forward(mtx, basecol, step, *cols):
    """
        forward interpolation for specified matrix columns on base column with step
    formula:
        yij = yi,
    where:
        (x, y) = [(x0, y0), (x1, y1), ..., (xn, yn)]
        i<ij<j
    :param mtx: matrix
    :param basecol: base column for interpolation
    :param step: step of base column for interpolation
    :param cols: columns to interpolate, default all columns will be interpolated
    :return: matrix
    """
    # default interpolate all columns
    if len(cols)==0:
        cols = list(range(1, dtl.matrix.numcols(mtx)+1))

    # get the base column's indexs in output results
    basecolidxs = _indexs(cols, basecol)

    # interpolation result
    interpmtx = []

    # process all records
    last_row = None
    for row in mtx:
        # first remember the last row
        if last_row is None:
            last_row = row
            interpmtx.append([row[i-1] for i in cols])
            continue

        # steps between last row with current row
        steps = int((row[basecol-1]-last_row[basecol-1])/step)-1

        # interpolate with forward value for all steps
        for stp in range(1, steps+1):
            # interpolate use forward value
            interprow = [last_row[i-1] for i in cols]

            # change base column value in interpolated row
            if basecolidxs is not None:
                for idx in basecolidxs:
                    interprow[idx] = interprow[idx]+stp*step

            # add to result
            interpmtx.append(interprow)

        # add current row to result
        interpmtx.append([row[i-1] for i in cols])

        # change last row
        last_row = row

    return interpmtx


def backward(mtx, basecol, step, *cols):
    """
        backward interpolation for specified matrix columns on base column with step
    formula:
        yij = yj,
    where:
        (x, y) = [(x0, y0), (x1, y1), ..., (xn, yn)]
        i<ij<j
    :param mtx: matrix
    :param basecol: base column for interpolation
    :param step: step of base column for interpolation
    :param cols: columns to interpolate, default all columns will be interpolated
    :return: matrix
    """
    # default interpolate all columns
    if len(cols)==0:
        cols = list(range(1, dtl.matrix.numcols(mtx)+1))

    # get the base column's indexs in output results
    basecolidxs = _indexs(cols, basecol)

    # interpolation result
    interpmtx = []

    # process all records
    last_row = None
    for ridx in range(len(mtx)-1, -1, -1):
        # current row
        row = mtx[ridx]

        # first remember the last row
        if last_row is None:
            last_row = row
            interpmtx.append([row[i-1] for i in cols])
            continue

        # steps between last row with current row
        steps = int((last_row[basecol-1]-row[basecol-1])/step)-1

        # interpolate with forward value for all steps
        for stp in range(1, steps+1):
            # interpolate use forward value
            interprow = [last_row[i-1] for i in cols]

            # change base column value in interpolated row
            if basecolidxs is not None:
                for idx in basecolidxs:
                    interprow[idx] = interprow[idx]-stp*step

            # add to result
            interpmtx.append(interprow)

        # add current row to result
        interpmtx.append([row[i-1] for i in cols])

        # change last row
        last_row = row

    # reverse the result
    interpmtx.reverse()

    return interpmtx


if __name__ == "__main__":
    import dtl
    mtx = [
        [dtl.time.day("20170125", "%Y%m%d"), 25, 25, 25],
        [dtl.time.day("20170128", "%Y%m%d"), 28, 28, 28],
        [dtl.time.day("20170201", "%Y%m%d"), 1, 1, 1],
        [dtl.time.day("20170205", "%Y%m%d"), 5, 5, 5]
    ]
    print("input matrix: ")
    print(mtx)

    print("after linear interpolation: ")
    print(linear(mtx, 1, 1, 1, 2, 3))

    print("after forward interpolation: ")
    print(forward(mtx, 1, 1, 1, 2, 3))

    print("after backward interpolation: ")
    print(backward(mtx, 1, 1, 1, 2, 3))

