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

    def add(self, cols):
        self._cols.update(cols)
        for name, value in cols.items():
            self._table.col(name).row_add(self._name, value)
        return self

    def col_add(self, name, value):
        self._cols[name] = value

    def col(self, name, default=None):
        return self._cols.get(name, default)

    def columns(self):
        return self._cols.keys()

    def values(self, default=None):
        values = []
        for ncol in self._table.ncols():
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

    def add(self, rows):
        self._rows.update(rows)
        for name, value in rows.items():
            self._table.row(name).col_add(self._name, value)
        return self

    def row_add(self, name, value):
        self._rows[name] = value

    def row(self, name, default=None):
        return self._rows.get(name, default)

    def rows(self):
        return self._rows.keys()

    def values(self, default=None):
        values = []
        for nrow in self._table.nrows():
            values.append(self._rows.get(nrow, default))
        return values


class Table:
    def __init__(self):
        self._nrows = {}
        self._ncols = {}

        self._rows = {}
        self._cols = {}

    def __str__(self):
        WIDTH, formatted_strs = 10, []
        # column name string
        formatted_ncols = [''.center(WIDTH, ' ')]
        for ncol in self._ncols.keys():
            formatted_ncols.append(str(ncol).center(WIDTH, ' '))
        formatted_strs.append(''.join(formatted_ncols))

        # row name string
        formatted_nrows = []
        for nrow in self._nrows.keys():
            formatted_nrows.append(str(nrow).center(WIDTH, ' '))

        # row value string
        ncolnum = 0
        for row in self._rows.values():
            formatted_vcols = [formatted_nrows[ncolnum]]
            for vcol in row.values():
                formatted_vcols.append(str(vcol).center(WIDTH, ' '))
            formatted_strs.append(''.join(formatted_vcols))
            ncolnum += 1

        # table string
        return '\n'.join(formatted_strs)

    def __repr__(self):
        return self.__str__()

    def row(self, name):
        row = self._rows.get(name)
        if row is None:
            self._rows[name] = Row(name, self)
            self._nrows[name] = name
        return self._rows.get(name)

    def col(self, name):
        col = self._cols.get(name)
        if col is None:
            self._cols[name] = Column(name, self)
            self._ncols[name] = name
        return self._cols.get(name)

    def rows(self):
        values = []
        for row in self._rows:
            values.append(row.values())
        return values

    def cols(self):
        values = []
        for col in self._cols:
            values.append(col.values())
        return values

    def nrows(self):
        return self._nrows.keys()

    def ncols(self):
        return self._ncols.keys()

if __name__ == "__main__":
    table = Table()

    table.col("price").add({'20150103':1.01, '20150104':1.02, '20150105':1.03})
    table.col("rate").add({'20150103':2.01, '20150104':2.02, '20150105':2.03})
    table.col("rate1").add({'20150103': 2.07, '20150104': 2.08, '20150106': 2.09})
    table.row("rate1").add({'20150103': 3.07, '20150104': 3.08, '20150106': 3.09})

    print(table)

    print(table.row('rate1').col('201501'))