"""
    matrix for data process
"""


class Row:
    def __init__(self, matrix):
        self._matrix = matrix
        self._cols = []

    def add(self, *col):
        #add column values in row
        self._cols += col

    def col(self, num):
        return self.cols[num-1]

    def cols(self):
        return self._cols


class Column:
    def __init__(self, matrix):
        self._matrix = matrix
        self._rows = []

    def add(self, *row):
        self._rows += row

    def row(self, num):
        return self._rows[num-1]

    def rows(self):
        return self._rows


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

    def row(self, num):
        # add new row
        if len(self._rows)<num:
            self._rows.append(Row(self))

        # return row at @num
        return self._rows[num-1]

    def col(self, num):
        # add new column
        if len(self._cols)<num:
            self._cols.append(Column(self))

        # return column at @num
        return self._cols[num-1]


if __name__ == "__main__":
    matrix = Matrix()
    matrix.row(1).add(1, 2, 3)
    matrix.row(2).add(4, 5, 6)
    matrix.row(3).add(7, 8, 9)

    print(matrix)