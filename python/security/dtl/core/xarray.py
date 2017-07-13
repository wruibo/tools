"""
    array for data process
"""
'''
    useful array data process functions
'''
import math


class xiterarr:
    def __init__(self, data):
        self._data = data
        self._pos = 0

    def __next__(self):
        if self._pos == len(self._data):
            raise StopIteration()

        nextitem = self._data[self._pos]
        self._pos += 1
        return nextitem


class xarray(object):
    """
        array class for holding array data, like:
        [item1, item2, item3, ...]
    """
    def __init__(self, data=[]):
        self._data = data

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return xiterarr(self._data)

    def __len__(self):
        return len(self._data)

    @property
    def data(self):
        return self._data

    def avg(self):
        """
        compute average of sample values
        :param values: list, list of sample values
        :return: float, average of sample values
        """
        if len(self._data) == 0:
            return

        return float(sum(self._data)) / len(self._data)

    def var(self):
        """
        compute variance of sample values
        :param values: list, list of sample values
        :return: float, variance of sample values
        """
        if len(self._data) == 0:
            return

        # use average value of values as the expect value
        expect_value = self.avg()

        sum = 0.0
        for value in self._data:
            sum += (value - expect_value) ** 2

        return sum / (len(self._data) - 1)

    def stddev(self):
        '''
        compute standard deviation of sample values
        :param values: list, list of sample values
        :return: float, standard deviation of sample values
        '''
        if len(self._data) == 0:
            return

        return math.sqrt(self.var())

    def cov(self, other):
        """
        compute the covariance of sample a1 and a2
        :param a1: list, list of input data values
        :param a2: list, list of input data values
        :return: float, covariance of sample a1 and a2
        """
        if len(self) != len(other):
            return None

        expect_value1 = self.avg()
        expect_value2 = other.avg()

        sum = 0.0
        idx = num = len(self)
        while idx > 0:
            idx -= 1
            sum += (self._data[idx] - expect_value1) * (other.data[idx] - expect_value2)

        return sum / (num - 1)

    def cor(self, other):
        """
         compute the correlation of sample a1 and a2, using pearson correlation algorithm
         :param a1: list, list of input data values
         :param a2: list, list of input data values
         :return:
        """
        if len(self) != len(other):
            return None

        # compute covariance of a1 and a2
        cov12 = self.cov(other)

        # compute the standard deviation of a1, a2
        stddev1 = self.stddev()
        stddev2 = other.stddev()

        return cov12 / (stddev1 * stddev2)
