"""
    table structure definition
"""
from utl import type as _type
from utl import date as _date


__all__ = ["Model", "Field", "IntField", "FloatField", "StringField", "DateField", "ObjectField"]


class Field(object):
    """
        field for model
    """
    def __init__(self, type, default, *args):
        """
            initialize field
        :param typecls: class or function, convert original value to
        :param args: tuple, args pass to @typecls
        """
        self._type = type
        self._default = default
        self._args = args

    def __call__(self, value=None):
        """
            call for convert original value to define value of model
        :param args:
        :param kwargs:
        :return:
        """
        if self._type is None:
            return value

        if value is None:
            value = self._default

        return self._type(value, *self._args) if len(self._args)>0 else self._type(value)


class IntField(Field):
    def __init__(self, default=0, base=10):
        super(IntField, self).__init__(_type.int, default, base)


class FloatField(Field):
    def __init__(self, default=0.0):
        super(FloatField, self).__init__(_type.float, default)


class StringField(Field):
    def __init__(self, default=''):
        super(StringField, self).__init__(_type.string, default)


class DateField(Field):
    def __init__(self, format):
        super(DateField, self).__init__(_date.date, None, format)


class ObjectField(Field):
    def __init__(self):
        super(ObjectField, self).__init__(None, None)


class ModelMetaClass(type):
    """
        meta class of models
    """
    def __new__(cls, name, parents, attrs):
        if name == "Model":
            return type.__new__(cls, name, parents, attrs)

        # field names and types of model
        fields = {}

        # process all fields
        for name, value in attrs.items():
            if isinstance(value, Field):
                fields[name] = value

        for field in fields.keys():
            attrs.pop(field)

        # save the fields to attributes
        attrs['__fields__'] = fields

        return type.__new__(cls, name, parents, attrs)


class Model(dict, metaclass=ModelMetaClass):
    """
        base class of models
    """
    def __init__(self, **kwargs):
        for key, values in kwargs.items():
            if self.__fields__.get(key) is not None:
                for value in values:
                    if self.get(key) is None:
                        self[key] = []
                    self[key].append(self.__fields__[key](value))
            else:
                self[key] = values

    def __setattr__(self, key, values):
        if self.__fields__.get(key) is not None:
            for value in values:
                if self.get(key) is None:
                    self[key] = []
                self[key].append(self.__fields__[key](value))
        else:
            self[key] = values

    def __getattr__(self, key):
        return self.get(key)

    def titles(self):
        """
            get table column titles
        :return:
        """
        return list(self.keys())

    def rows(self):
        """
            get table data by rows
        :return:
        """
        rows = []
        columns = list(self.values())
        for column in columns:
            rownum = 1
            for item in column:
                if len(rows) < rownum:
                    rows.append([])
                rows[rownum-1].append(item)
                rownum += 1
        return rows

    def columns(self):
        """
            get table data by columns
        :return:
        """
        return list(self.values())
