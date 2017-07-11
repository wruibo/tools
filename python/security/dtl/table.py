"""
    table for holding data
"""


class Table:
    """
        table base class for holding table data, like:
             col1   col2  ...  colN
        row1  X11    X12  ...   X1N
        row2  X21    X22  ...   X2N
          .    .      .          .
          .    .      .          .
          .    .      .          .
        rowM  XM1    XM2  ...   XMN

        the table data can be storage by row data, column data, or named row/column data
    """
    def __init__(self):
        pass

    def rrows(self, *rows):
        """
             get one or multi rows from table by specified row numbers @rows
         :param rows: row numbers want to get
         :return: rows got from table
         """
        pass

    def rcols(self, *cols):
        """
            get all rows by specified column numbers @cols from table
        :param cols: column numbers
        :return: all rows got from table
        """
        pass

    def crows(self, *rows):
        """
            get all columns by specified row numbers @rows from table
        :param rows: row numbers
        :return: all columns got from table
        """
        pass

    def rcols(self, *cols):
        """
            get one or multi columns from row storage table
        :param cols: column numbers(start from 1) want to get
        :return:
        """
        pass


class RTable(Table):
    """
        table with rows storage, format:
        [
            [R11    R12  ...   R1N],
            [R21    R22  ...   R2N],
            [.    .      .      .],
            [.    .      .      .],
            [.    .      .      .],
            [RM1    RM2  ...  RMN]
        ]
    """
    def __init__(self, rows=[[]]):
        """
            init table with row storage structure
        :param rows:
        """
        self._rows = rows

    def __str__(self):
        # every formatted rows and item width in character
        srows, SEP, WIDTH = [], ',', 12

        # format every row values
        for row in self._rows:
            scols = []
            for col in row:
                scols.append(str(col).center(WIDTH, ' '))
            srows.append(SEP.join(scols))

        # format all row values
        return '\n'.join(srows)

    def __repr__(self):
        return self.__str__()

    def rrows(self, *rows):
        """
            get one or multi rows by specified row numbers @rows from table
        :param rows: row numbers(start from 1) want to get
        :return: rows got from table
        """
        # default get all rows
        if len(rows)==0:
            return self._rows

        # get the specified @rows
        results = []
        for rnum in rows:
            results.append(self._rows[rnum-1])

        # return row < [] > or rows < [[]] >
        return results if len(results)>1 else results[0]

    def rcols(self, *cols):
        """
            get all rows by specified column numbers @cols from table
        :param cols: column numbers
        :return: all rows got from table
        """
        if len(cols)==0:
            return self._rows

        results = []
        for row in self._rows:
            rvals = []
            for c in cols:
                rvals.append(row[c-1])
            results.append(rvals)

        return results

    def crows(self, *rows):
        """
            get all columns by specified row numbers @rows from table
        :param rows: row numbers
        :return: all columns got from table
        """
        if len(rows)==0:
            rows = range(1, len(self._rows)+1)

        results = []
        for cnum in range(1, len(self._rows[0])+1):
            cvals = []
            for rnum in rows:
                cvals.append(self._rows[rnum-1][cnum-1])
            results.append(cvals)

        return results

    def ccols(self, *cols):
        """
            get one or multi columns from row storage table
        :param cols: column numbers(start from 1) want to get
        :return:
        """
        # default get all columns
        if len(cols)==0:
            cols = range(1, len(self._rows[0])+1)

        # get all specified @columns
        results = []
        for cnum in cols:
            cvals = []
            for row in self._rows:
                cvals.append(row[cnum-1])
            results.append(cvals)

        # return column < [] > or columns < [[]] >
        return results if len(results)>1 else results[0]


class CTable(Table):
    """
        table with columns storage, format:
        [
            [C11    C12  ...   C1N],
            [C21    C22  ...   C2N],
            [.      .    .      .],
            [.      .    .      .],
            [.      .    .      .],
            [CM1    CM2  ...   CMN]
        ]
    """
    def __init__(self, cols=[[]]):
        """
            init table with columns storage structure
        :param cols:
        """
        self._cols = cols

    def __str__(self):
        # row strings to print and item width in character
        srows, SEP, WIDTH = [], ',', 12

        # format every row values
        for rnum in range(0, len(self._cols[0])):
            rvals = []
            for col in self._cols:
                rvals.append(str(col[rnum]).center(WIDTH, ' '))
            srows.append(SEP.join(rvals))

        # format all row values
        return '\n'.join(srows)

    def __repr__(self):
        return self.__str__()

    def rrows(self, *rows):
        """
            get one or multi rows from row storage table
        :param rows: row numbers(start from 1) want to get
        :return: rows got from table
        """
        # default get all rows
        if len(rows)==0:
            rows = range(1, len(self._cols[0])+1)

        # get the specified @rows
        results = []
        for rnum in rows:
            rvals = []
            for col in self._cols:
                rvals.append(col[rnum-1])
            results.append(rvals)

        # return row < [] > or rows < [[]] >
        return results if len(results)>1 else results[0]

    def rcols(self, *cols):
        """
            get all rows by specified column numbers @cols from table
        :param cols: column numbers
        :return: all rows got from table
        """
        if len(cols) == 0:
            cols = range(1, len(self._cols)+1)

        results = []
        for rnum in range(1, len(self._cols[0])+1):
            rvals = []
            for c in cols:
                rvals.append(self._cols[c-1][rnum-1])
            results.append(rvals)

        return results

    def crows(self, *rows):
        """
            get all columns by specified row numbers @rows from table
        :param rows: row numbers
        :return: all columns got from table
        """
        if len(rows) == 0:
            return self._cols

        results = []
        for col in self._cols:
            cvals = []
            for rnum in rows:
                cvals.append(col[rnum])
            results.append(cvals)

        return results

    def ccols(self, *cols):
        """
            get one or multi columns from row storage table
        :param cols: column numbers(start from 1) want to get
        :return:
        """
        # default get all columns
        if len(cols)==0:
            return self._cols

        # get all specified @columns
        results = []
        for cnum in cols:
            results.append(self._cols[cnum-1])

        # return column < [] > or columns < [[]] >
        return results if len(results)>1 else results[0]


class Row:
    def __init__(self, name, table):
        self._table = table
        self._name = name
        self._cols = {}

    @property
    def name(self):
        return self._name

    def col(self, name, value=None):
        # return column value of @name in row
        if value is None:
            return self._cols.get(name)

        # set column value of @name in row
        self._cols[name] = value

    def cols(self, cols=None):
        # return column values of row
        if cols is None:
            values = []
            for ncol in self._table.col_names():
                values.append(self._cols.get(ncol))
            return values

        # set column values of row
        self._cols.update(cols)
        for name, value in cols.items():
            self._table.col(name).row(self._name, value)
        return self


class Column:
    def __init__(self, name, table):
        self._table = table
        self._name = name
        self._rows = {}

    @property
    def name(self):
        return self._name

    def row(self, name, value=None):
        # return row value of @name in column
        if value is None:
            return self._rows.get(name)

        # set row value of @name in column
        self._rows[name] = value

    def rows(self, rows=None):
        # return row values of column
        if rows is None:
            values = []
            for nrow in self._table.row_names():
                values.append(self._rows.get(nrow))
            return values

        # set row values of column
        self._rows.update(rows)
        for name, value in rows.items():
            self._table.row(name).col(self._name, value)
        return self


class NTable(Table):
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

    def rrows(self, *names):
        """
            extract row values from table, or extract specified rows if @names given, results:
            [
                [c11, c12, c13, ...],
                [c21, c22, c23, ...],
                [c31, c32, c33, ...],
            ]
        :param rows: row names specified
        :return: list with row's column values
        """
        if len(names)==0:
            names = self._rows.keys()

        values = []
        for name in names:
            values.append(self._rows[name].cols())

        return values

    def ccols(self, *names):
        """
            extract column values from table, or extract specified columns if @names given, results:
            [
                [r11, r12, r13, ...],
                [r21, r22, r23, ...],
                [r31, r32, r33, ...],
            ]
        :param columns: column names specified
        :return: list with column's row values
        """
        if len(names)==0:
            columns = self._cols.keys()

        values = []
        for name in names:
            values.append(self._cols[name].rows())

        return values

    def row_names(self):
        return self._rows.keys()

    def col_names(self):
        return self._cols.keys()

if __name__ == "__main__":
    table = NTable()

    table.col("abc").rows({'1': 2.07, '2': 2.08, '3': 2.09})
    table.col("price").rows({'1':1.01, '2':1.02, '3':1.03})
    table.col("rate").rows({'1':2.01, '2':2.02, '3':2.03})
    table.row("rate1").cols({'1': 3.07, '2': 3.08, '3': 3.09})

    print(table)

    print(table.row('rate1').col('2'))
    print("------")
    print(table.rows("1", "2"))
    print("------")
    print(table.cols("1", "2"))