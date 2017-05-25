'''
    table for store
'''
from store import *
from store.type import *
from store.value import *
from store.field import *
from store.verifier import *


class MetaTable(type):
    '''
        meta class of table
    '''
    def __new__(cls, name, bases, attrs):
        if name == 'Table':
            attrs['name'] = None
            attrs['fields'] = []
            attrs['keys'] = []
            return type.__new__(cls, name, bases, attrs)

        #process fields and keys of table
        fields, keys = [], []
        for name, value in attrs.items():
            if isinstance(value, Field):
                if value.name is None:
                    value.name = name
                fields.append(value)
                attrs.pop(name)
            elif issubclass(value.__class__, Key):
                if value.name is None:
                    value.name = name
                keys.append(value)
                attrs.pop(name)
            else:
                pass

        #order the fields and keys
        fields.sort()
        keys.sort()

        #process table name
        table_name = "tb"
        for s in name:
            if s.isupper():
                table_name = "%s_%s" % (table_name, s.lower())
            else:
                table_name = "%s%s" % (table_name, s)

        #set the table name, fields, keys attributes
        attrs['name'] = table_name
        attrs['fields'] = fields
        attrs['keys'] = keys

        return type.__new__(cls, name, bases, attrs)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name==other.name and self.fields == other.fields
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Table:
    '''
        base table class for store
    '''
    __metaclass__ = MetaTable

    def __init__(self, name=None):
        if name is not None:
            self.name = name

    def nfields(self):
        names = []
        for field in self.fields:
            names.append(field.name)
        return names

    def nkeys(self):
        names = []
        for key in self.keys:
            names.append(key.name)
        return names

    def match(self, model):
        return True

    def tosql(self):
        '''
            translate table to create sql
        :return:
        '''
        #field sql
        sql_fields = []
        for field in self.fields:
            sql_fields.append("\t%s" % field.tosql())
        sql_fields = ",\n".join(sql_fields)

        #key sql
        sql_keys = []
        for key in self.keys:
            sql_keys.append("\t%s" % key.tosql())
        sql_keys = ",\n".join(sql_keys)

        #table sql
        if sql_keys:
            sql_table = "create table if not exists `%s`\n(\n%s,\n%s\n);" % (self.name, sql_fields, sql_keys)
        else:
            sql_table = "create table if not exists `%s`\n(\n%s\n);" % (self.name, sql_fields)

        return sql_table

    def fromsql(self, sql):
        '''
            create table from sql
        :param sql:
        :return:
        '''
        regex_name = re.compile(r'\s*create\s+table\s+'
                                r'[^\(]*'
                                r'`(\w+)`\s*\(',
                                re.IGNORECASE)

        regex_fields = re.compile(r'('
                                  r'`[\w_]+`\s+'
                                  r'\w+'
                                  r'(\([^\(\)]+\))?\s+'
                                  r'[^,]*'
                                  r')',
                                  re.IGNORECASE)

        regex_keys = re.compile(r'('
                                r'(unique\s+|primary\s+)?'
                                r'key\s*'
                                r'(`?[\w_]+`?\s*)?'
                                r'\([^\(\)]+\)'
                                r')',
                                re.IGNORECASE)

        #extract table name
        mobj = regex_name.match(sql)
        if mobj:
            self.name = mobj.group(1)

        #extract fields
        mobjs = regex_fields.findall(sql)
        for mobj in mobjs:
            self.fields.append(Field().fromsql(mobj[0]))

        #extract keys
        mobjs = regex_keys.findall(sql)
        for mobj in mobjs:
            self.keys.append(Key().fromsql(mobj[0]))

        return self


    def tostr(self):
        '''
            translate schema to string
        :param schema:
        :return:
        '''
        #translate name
        sname = "[table]\nname=%s\n" % self.name

        #translate fields
        sfields = "[fields]\n"
        for field in self.fields:
            sfield = "%s\n" % field.tostr()
            sfields += sfield

        #translate keys
        skeys = "[keys]\n"
        for key in self.keys:
            skey = "%s\n" % key.tostr()
            skeys += skey

        return "%s%s%s" % (sname, sfields, skeys)

    def fromstr(self, str):
        '''
            translate string to schema object
        :param str:
        :return:
        '''
        regex_section = re.compile("^\s*\[\s*(?P<section>\w+)\s*\]\s*$")
        regex_name = re.compile("\s*name\s*=\s*(?P<name>\w+)\s*")
        section = None
        lines = str.splitlines()
        for line in lines:
            if line.strip() == '':
                continue


            msec = regex_section.match(line)
            if msec:
                section = msec.group('section')
                section = section.lower()
            else:
                if section:
                    if section == 'table':
                        mname = regex_name.match(line)
                        if mname:
                            self.name = mname.group('name')
                    elif section == 'fields':
                        self.fields.append(Field().fromstr(line))
                    elif section == 'keys':
                        self.keys.append(Key().fromstr(line))
                    else:
                        pass
                else:
                    pass
        return self

if __name__ == "__main__":
    pass