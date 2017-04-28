'''
    schema for table creation
'''
import re

from storage.ckey import *
from storage.ctype import *
from storage.cindex import *
from storage.cvalue import *
from storage.cfield import *
from storage.cverifier import *


class Schema:
    def __init__(self, name=None):
        self.name = name

        self.fields = []
        self.keys = []
        self.indexs = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name==other.name and self.fields == other.fields and self.keys==other.keys and self.indexs==other.indexs
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def field(self, name, type, nullable=True, default=NullValue(), verifier=DefaultVerifier()):
        self.fields.append(Field(name, type, nullable, default, verifier))

    def key(self, keycls, name, *fields):
        self.keys.append(keycls(name, *fields))

    def index(self, indexcls, name, *fields):
        self.indexs.append(indexcls(self.name, name, *fields))

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

    def nindexs(self):
        names = []
        for index in self.indexs:
            names.append(index.name)
        return names

    def match(self, record):
        return True

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

        #translate indexs
        sindexs = "[indexs]\n"
        for index in self.indexs:
            sindex = "%s\n" % index.tostr()
            sindexs += sindex

        #translate keys
        skeys = "[keys]\n"
        for key in self.keys:
            skey = "%s\n" % key.tostr()
            skeys += skey

        return "%s%s%s%s" % (sname, sfields, sindexs, skeys)

    def fromstr(self, str):
        '''
            translate string to schema object
        :param str:
        :return:
        '''
        SectionRegex = re.compile("^\s*\[\s*(?P<section>\w+)\s*\]\s*$")
        NameRegex = re.compile("\s*name\s*=\s*(?P<name>\w+)\s*")
        section = None
        lines = str.splitlines()
        for line in lines:
            if line.strip() == '':
                continue


            msec = SectionRegex.match(line)
            if msec:
                section = msec.group('section')
                section = section.lower()
            else:
                if section:
                    if section == 'table':
                        mname = NameRegex.match(line)
                        if mname:
                            self.name = mname.group('name')
                    elif section == 'fields':
                        self.fields.append(Field().fromstr(line))
                    elif section == 'keys':
                        self.keys.append(Key().fromstr(line))
                    elif section == 'indexs':
                        self.indexs.append(Index().fromstr(line))
                    else:
                        pass
                else:
                    pass
        return self

if __name__ == "__main__":
    schema = Schema("tb_demo")
    schema.field("id", Int(), False, AutoIncValue())
    schema.field("code", String(32), False)
    schema.field("name", String(32), True)
    schema.field("valid", Boolean(), True)
    schema.field("create_time", BigInt(), True)

    schema.key(PrimaryKey, "pk_id", "id")
    schema.key(NormalKey, "normal_key", "name","code")
    schema.key(UniqueKey, "unique_key", "code", "valid")

    schema.index(NormalIndex, "normal_index", "name", "code")
    schema.index(UniqueIndex, "unique_index", "code", "valid")

    str1 = schema.tostr()
    print str1

    print Schema().fromstr(str1).tostr()
