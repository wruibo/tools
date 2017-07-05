"""
    table for holding data, format:
         row1   row2  ...  rowN
    col1  X11    X12  ...   X1N
    col2  X21    X22  ...   X2N
      .    .      .          .
      .    .      .          .
      .    .      .          .
    colM  XM1    XM2  ...   XMN
"""


class Row:
    def __init__(self, name, table):
        self._table = table
        self._name = name
        self._cols = {}

    @property
    def name(self):
        return self._name

    def add_cols(self, cols):
        self._cols.update(cols)
        for name, value in cols.items():
            self._table.col(name).add_row(self._name, value)
        return self

    def add_col(self, name, value):
        self._cols[name] = value

    def col(self, name, default=None):
        return self._cols.get(name, default)

    def cols(self, default=None):
        values = []
        for ncol in self._table.col_names():
            values.append(self._cols.get(ncol, default))
        return values


class Column:
    def __init__(self, name, table):
        self._table = table
        self._name = name
        self._rows = {}

    @property
    def name(self):
        return self._name

    def add_rows(self, rows):
        self._rows.update(rows)
        for name, value in rows.items():
            self._table.row(name).add_col(self._name, value)
        return self

    def add_row(self, name, value):
        self._rows[name] = value

    def row(self, name, default=None):
        return self._rows.get(name, default)

    def rows(self, default=None):
        values = []
        for nrow in self._table.row_names():
            values.append(self._rows.get(nrow, default))
        return values


class Table:
    def __init__(self):
        self._rows = {}
        self._cols = {}

    def __str__(self):
        WIDTH, formatted_strs = 10, []
        # column name string
        formatted_ncols = [''.center(WIDTH, ' ')]
        for ncol in self._cols.keys():
            formatted_ncols.append(str(ncol).center(WIDTH, ' '))
        formatted_strs.append(''.join(formatted_ncols))

        # row name string
        formatted_nrows = []
        for nrow in self._rows.keys():
            formatted_nrows.append(str(nrow).center(WIDTH, ' '))

        # row value string
        ncolnum = 0
        for row in self._rows.values():
            formatted_vcols = [formatted_nrows[ncolnum]]
            for vcol in row.cols():
                formatted_vcols.append(str(vcol).center(WIDTH, ' '))
            formatted_strs.append(''.join(formatted_vcols))
            ncolnum += 1

        # table string
        return '\n'.join(formatted_strs)

    def __repr__(self):
        return self.__str__()

    def row(self, name):
        """
            get row object by row @name
        :param name: row name
        :return: @Row object
        """
        row = self._rows.get(name)
        if row is None:
            self._rows[name] = Row(name, self)
        return self._rows.get(name)

    def col(self, name):
        """
            get column object by column @name
        :param name: column name
        :return: @Column object
        """
        col = self._cols.get(name)
        if col is None:
            self._cols[name] = Column(name, self)
        return self._cols.get(name)

    def rows(self, *rows):
        """
            extract row values from table, or extract specified rows if @rows given, results:
            [
                [c11, c12, c13, ...],
                [c21, c22, c23, ...],
                [c31, c32, c33, ...],
            ]
        :param rows: row names specified
        :return: list with row's column values
        """
        if len(rows)==0:
            rows = self._rows.keys()

        values = []
        for row in rows:
            values.append(self._rows[row].cols())

        return values

    def cols(self, *columns):
        """
            extract column values from table, or extract specified columns if @columns given, results:
            [
                [r11, r12, r13, ...],
                [r21, r22, r23, ...],
                [r31, r32, r33, ...],
            ]
        :param columns: column names specified
        :return: list with column's row values
        """
        if len(columns)==0:
            columns = self._cols.keys()

        values = []
        for column in columns:
            values.append(self._cols[column].rows())

        return values

    def row_names(self):
        return self._rows.keys()

    def col_names(self):
        return self._cols.keys()

if __name__ == "__main__":
    table = Table()

    table.col("abc").add_rows({'1': 2.07, '2': 2.08, '3': 2.09})
    table.col("price").add_rows({'1':1.01, '2':1.02, '3':1.03})
    table.col("rate").add_rows({'1':2.01, '2':2.02, '3':2.03})
    table.row("rate1").add_cols({'1': 3.07, '2': 3.08, '3': 3.09})

    print(table)

    print(table.row('rate1').col('2'))
    print("------")
    print(table.rows("1", "2"))
    print("------")
    print(table.cols("1", "2"))