'''
    field for define table
'''
import re

from utility.ccast import *

from storage.ctype import *
from storage.cvalue import *
from storage.cverifier import *


class Field:
    def __init__(self, name=None, type=None, default=DefaultNull(), verifier=DefaultVerifier()):
        self.name = name
        self.type = type
        self.default = default
        self.verifier = verifier

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name==other.name and self.type==other.type
        return False

    def verify(self, value):
        return self.verifier.verify(value)

    def tosql(self):
        return "%s %s %s" % (self.name, self.type.tosql(), self.default.tosql())

    def fromsql(self, sql):
        sql = sql.strip()
        regex_feild = re.compile(r'`(?P<name>\w+)`\s+(?P<type>\w+(\([,\d\s]+\))?)(?P<default>[^,\)]+)?')
        mobj = regex_feild.match(sql)
        if mobj:
            sname, stype, sdefault = mobj.group('name', 'type', 'default')
            self.name, self.type, self.default = sname, Type().fromsql(stype), Value().fromsql(sdefault)
            return self

    def tostr(self):
        return "name=%s;type=%s;default=%s" % (self.name, self.type.tostr(), self.default.tostr())

    def fromstr(self, str):
        regex_field = re.compile(r'^\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*type\s*=\s*(?P<type>.+)\s*;\s*default\s*=\s*(?P<default>.+)\s*$')
        mobj = regex_field.match(str)
        if mobj:
            sname, stype, sdefault = mobj.group('name', 'type', 'default')
            self.name, self.type, self.default = sname, Type().fromstr(stype), Value().fromstr(sdefault)
            return self


if __name__ == "__main__":
    field1 = Field("id", Int(), AutoIncValue())
    field2 = Field("code", String(32))
    field3 = Field("name", String(32), StringValue('name'))
    field4 = Field("valid", Boolean(), BooleanValue(True))
    field5 = Field("create_time", BigInt())

    if field1 == field2:
        print "hello"

    print field1.tostr()
    print field2.tostr()
    print field3.tostr()
    print field4.tostr()
    print field5.tostr()

    print Field().fromstr(field1.tostr()).tostr()
    print Field().fromstr(field2.tostr()).tostr()
    print Field().fromstr(field3.tostr()).tostr()
    print Field().fromstr(field4.tostr()).tostr()
    print Field().fromstr(field5.tostr()).tostr()

