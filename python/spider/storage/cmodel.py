'''
    model class
'''
from storage.ctable import Table

class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        #set the model attributes&fields from table
        fields = {}
        for key, value in attrs.items():
            if issubclass(value.__class__, Table):
                for field in value.fields:
                    fields[field.name] = field
        #set fields declare and items
        attrs['fields'] = fields

        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kwargs):
        pass

class Model(dict):
    __metaclass__ = MetaModel

    def __init__(self, **kwargs):
        for name, field in self.fields.items():
            self[name] = field.default.default()

        for key in kwargs.keys():
            self[key] = kwargs.get(key, self.fields[key].default.default())

    def __getattr__(self, name):
        return self.get(name, self.fields[name].default.default())

    def __setattr__(self, name, value):
        self[name] = value

if __name__ == "__main__":
    pass
