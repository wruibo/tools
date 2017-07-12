"""
    table for holding data
"""


class xitertbl:
    def __init__(self, data):
        self._data = data
        self._nextrow = 0

    def __next__(self):
        if self._nextrow == len(self._data):
            raise StopIteration()

        nextrow = self._data[self._nextrow]
        self._nextrow += 1
        return nextrow


class xtable(object):
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
    def __init__(self, data=[]):
        self._data = data

    def __str__(self):
        # every formatted rows and item width in character
        srows, SEP, WIDTH = [], ',', 12

        # format every row values
        for row in self._data:
            scols = []
            for col in row:
                scols.append(str(col).center(WIDTH, ' '))
            srows.append(SEP.join(scols))

        # format all row values
        return '\n'.join(srows)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return xitertbl(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, rownum):
        return self._data[rownum]

    @property
    def data(self):
        return self._data

    def append(self, rows):
        """
            append @rows data to end of current table
        :param rows: array of row
        :return: self
        """
        self._data.extend(rows)

        return self

    def extend(self, tbl):
        """
            extend @tbl data to end of current table
        :param tbl: xtable, table to be append
        :return: self
        """
        self._data.extend(tbl.data)

        return self

    def addrow(self, row):
        """
            add @row to table as last row
        :param row: array, row to be added to end
        :return: self
        """
        # new @row must be type of tuple or list
        if not (isinstance(row, list) or isinstance(row, tuple)):
            raise "add row's type must be list or tuple."

        # item count in row must be same as other rows in table
        if len(self._data)!=0 and len(row)!=len(self._data[0]):
            raise "add row's item count must be same as other rows."

        # add new @row to the end
        self._data.append(list(row))

        return self

    def delrow(self, num):
        """
            delete row with row number @num
        :param num: int, row number from 1
        :return: self
        """
        # delete nothing if table has no @num row
        if num>len(self._data):
            raise "delete an not exist row %d" % num

        # delete the row @num
        self._data.remove(self._data[num-1])

        return self

    def addcol(self, col):
        """
            add @col to table as last column
        :param col: array, column to be added to end
        :return: self
        """
        # new @col must be type of tuple or list
        if not (isinstance(col, list) or isinstance(col, tuple)):
            raise "col's type must be list or tuple."

        # item count in @col must be same as other columns in table
        if len(self._data)!=0 and len(col)!=len(self._data):
            raise "col's item count must be same as other columns."

        # add new column to table
        i = 0
        for row in self._data:
            row.append(col[i])
            i += 1

        return self

    def delcol(self, num):
        """
            delete column with column number @num
        :param num: int, column number from 1
        :return: self
        """
        # delete nothing if table has no @num column
        if len(self._data)==0 or num>len(self._data[0]):
            raise "delete an not exist column %d" % num

        # delete the column @num
        for row in self._data:
            row.remove(row[num-1])

        return self

    def insrow(self, where, row):
        """
            insert @row in row number @where
        :param where: int, row number from 1 for the new @row
        :param row: array, row to be inserted
        :return: self
        """
        # new @row must be type of tuple or list
        if not (isinstance(row, list) or isinstance(row, tuple)):
            raise "insert row's type must be list or tuple."

        # item count in row must be same as other rows in table
        if len(self._data)!=0 and len(row)!=len(self._data[0]):
            raise "insert row's item count must be same as other rows."

        # add new @row to the specified place
        where = where-1 if where>0 else where
        self._data.insert(where, list(row))

        return self

    def inscol(self, where, col):
        """
            insert @col in column number @where
        :param where: int, column number from 1 for the new column
        :param col: array, column to be inserted
        :return: self
        """
        # new @col must be type of tuple or list
        if not (isinstance(col, list) or isinstance(col, tuple)):
            raise "insert col's type must be list or tuple."

        # item count in row must be same as other rows in table
        if len(self._data)!=0 and len(col)!=len(self._data[0]):
            raise "insert col's item count must be same as other columns."

        # add new @col to the specified place
        i, where = 0, where-1 if where>0 else where
        for row in self._data:
            row.insert(where, col[i])
            i += 1

        return self

    def getrow(self, num):
        """
            get row by row number @num
        :param num: int, row number
        :return: array of data, row data
        """
        return self._data[num-1]

    def getcol(self, num):
        """
            get column by column number @num
        :param num: int, column number
        :return: array, column data
        """
        col = []

        for row in self._data:
            col.append(row[num-1])

        return col

    def getrows(self, *nums):
        """
            get rows by row numbers @nums
        :param nums: tuple, row numbers
        :return: array of row, rows
        """
        rows = []

        for num in nums:
            rows.append(self._data[num-1])

        return rows

    def getcols(self, *nums):
        """
            get columns by column numbers @cols
        :param nums: tuple, column numbers
        :return: array of column, columns
        """
        cols = []

        for num in nums:
            col = []
            for row in self._data:
                col.append(row[num-1])
            cols.append(col)

        return cols

    def subtbl(self, rows=None, cols=None):
        """
            get a sub table from current table by specified @rownums and @colnums
        :param rows: tuple or list, row numbers
        :param cols: tuple or list, column numbers
        :return: Table
        """
        if rows is None:
            rows = range(1, self.rowdims()+1)

        if cols is None:
            cols = range(1, self.coldims()+1)

        data = []

        for rownum in rows:
            newrow = []
            for colnum in cols:
                newrow.append(self._data[rownum-1][colnum-1])
            data.append(newrow)

        return xtable(data)

    def rotate(self, copy=True):
        """
            rotate the table with rows and columns
        :param copy: boolean, copy a new table when copy is True, otherwise rotate the table itself
        :return: Table, self or new copied rotate Table
        """
        newdata = []

        for colnum in range(0, len(self._data[0])):
            col = []
            for row in self._data:
                col.append(row[colnum])
            newdata.append(col)

        if copy:
            return xtable(newdata)
        else:
            self._data = newdata
            return self

    def castcol(self, num, cls, *args):
        """
            cast specified column @num to class type @cls with args passed to class init function
        :param num: int, column number
        :param cls: class, type cast to
        :param args: tuple, arguments passed to class init function
        :return: self
        """

        for row in self._data:
            row[num-1] = cls(row[num-1], *args)

        return self

    def castrow(self, num, cls, *args):
        """
            cast specified row @num to class type @cls with args passed to class init function
        :param num: int, row number
        :param cls: class, type cast to
        :param args: tuple, arguments passed to class init function
        :return:
        """
        row = self._data[num-1]
        for i in range(0, len(row)):
            row[i] = cls(row[i], *args)

        return self

    def clone(self, withdata=True):
        """
            clone a new table object
        :param copydata: boolean, copy data if True
        :return: table object
        """
        if withdata:
            return xtable(self._data.copy())

        return xtable()

    def rowdims(self):
        """
            get the row dimension
        :return: int, row dimension
        """
        return len(self._data)

    def coldims(self):
        """
            get the column dimension
        :return: int, column dimension
        """
        return len(self._data[0]) if len(self._data)>0 else 0

    def dimension(self):
        """
            get the table dimension
        :return: tuple,  (row dimension, column dimension)
        """
        return (self.rowdims(), self.coldims())

if __name__ == "__main__":
    t = xtable([[1,2,3], [4,5,6]])
    print(t)
    print(t.rotate())
    print(t[0][1])
    for i in t:
        print(i)