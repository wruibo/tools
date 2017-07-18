"""
    interpolation algorithms
"""
import atl


def linear(mtx, basecol, step, *cols):
    """
        linear interpolation for specified matrix columns on base column with step
    input:
        [
            [x0, y11, y12, ..., y1m]
            [x1, y21, y22, ..., y2m]
            [       ...        ]
            [xn, yn1, yn2, ..., ynm]
        ]

    :param mtx: matrix
    :param basecol: base column for interpolation
    :param step: step of base column for interpolation
    :param cols: columns to interpolate, default all columns will be interpolated
    :return: matrix
    """
    # default interpolate all columns
    if len(cols)==0:
        cols = list(range(1, atl.matrix.numcols(mtx)+1))

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

if __name__ == "__main__":
    import dtl
    mtx = [
        [dtl.xday("20170125", "%Y%m%d"), 25, 25, 25],
        [dtl.xday("20170128", "%Y%m%d"), 28, 28, 28],
        [dtl.xday("20170201", "%Y%m%d"), 1, 1, 1],
        [dtl.xday("20170205", "%Y%m%d"), 5, 5, 5]
    ]
    print("input matrix: ")
    print(mtx)

    print("after linear interpolation: ")
    print(linear(mtx, 1, 1, 1, 2, 3))
