"""
    matrix for data process
"""


class Row:
    def __init__(self, cols=[]):
        self._cols = cols

    def col(self, num):
        return self.cols[num-1]

    def cols(self, cols=None):
        if cols is None:
            return self._cols

        self._cols = cols


class Column:
    def __init__(self, rows=[]):
        self._rows = rows

    def row(self, num):
        return self._rows[num-1]

    def rows(self, rows=None):
        if rows is None:
            return self._rows
        self._rows = rows


class Matrix:
    def __init__(self):
        self._rows = [] # matrix presents by row storage
        self._cols = [] # matrix presents by column storage

    def __str__(self):
        # every formatted rows and item width in character
        str_rows, WIDTH = [], 10

        # format every row values
        for row in self._rows:
            str_cols = []
            for col in row.cols():
                str_cols.append(str(col).center(WIDTH, ' '))
            str_rows.append(''.join(str_cols))

        # format all row values
        return '\n'.join(str_rows)

    def __repr__(self):
        return self.__str__()

    def init(self, rows=None, cols=None):
        if not((rows is None) != (cols is None)):
            return

        # generate rows using columns
        if rows is None:
            rows = []
            for i in range(0, len(cols[0])):
                row = []
                for j in range(0, len(cols)):
                    row.append(cols[j][i])
                rows.append(row)

        # generate columns using rows
        if cols is None:
            cols = []
            for i in range(0, len(rows[0])):
                col = []
                for j in range(0, len(rows)):
                    col.append(rows[j][i])
                cols.append(col)

        # initialize the matrix with row values
        for i in range(1, len(rows) + 1):
            self.row(i).cols(rows[i - 1])

        # initialize the matrix with column values
        for i in range(1, len(cols)+1):
            self.col(i).rows(cols[i-1])

        return self

    def row(self, num):
        """
            get row specified by row @num, add new row if it is not exist
        :param num:  row number start from 1
        :return: @Row object
        """
        # add new row
        if len(self._rows)<num:
            self._rows.append(Row())

        # return row at @num
        return self._rows[num-1]

    def col(self, num):
        """
            get column specified by column @num, add new column if it is not exist
        :param num: column number start from 1
        :return: @Column object
        """
        # add new column
        if len(self._cols)<num:
            self._cols.append(Column())

        # return column at @num
        return self._cols[num-1]

    def rows(self, *numbers):
        """
            get rows by specified row @numbers, return all rows if not specified
        :param numbers: row numbers
        :return: rows with column data
        """
        if len(numbers)==0:
            numbers = range(1, len(self._rows)+1)

        rows = []

        for n in numbers:
            rows.append(self._rows[n-1].cols())

        return rows

    def cols(self, *numbers):
        """
            get columns by specified column @numbers, return all columns if not specified
        :param columns: column numbers
        :return: columns with row data
        """
        if len(numbers) == 0:
            numbers = range(1, len(self._cols) + 1)

        cols = []

        for n in numbers:
            cols.append(self._cols[n - 1].rows())

        return cols


if __name__ == "__main__":
    matrix = Matrix()
    matrix.row(1).cols([1, 2, 3])
    matrix.row(2).cols([4, 5, 6])
    matrix.row(3).cols([7, 8, 9])

    print(matrix)

    print(matrix.rows(1, 2))
    print(matrix.cols(1, 2))