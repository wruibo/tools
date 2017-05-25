'''
    model class
'''
from store.table import Table

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

class Model(dict):
    __metaclass__ = MetaModel

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            self[name] = value

    def __getattr__(self, name):
        value = self[name]
        if value is None:
            return self.fields[name].default.default()

    def __setattr__(self, name, value):
        self[name] = value

    def get(self, name):
        return dict.get(self, name, self.fields[name].default.default())

if __name__ == "__main__":
    pass
