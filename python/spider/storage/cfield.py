'''
    field for define table
'''
import re

from utility.ccast import *

from storage.ctype import *
from storage.cvalue import *
from storage.cverifier import *


class Field:
    def __init__(self, name=None, type=None, nullable=True, default=NullValue(), verifier=DefaultVerifier()):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.default = default
        self.verifier = verifier

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name==other.name and self.type==other.type
        return False

    def verify(self, value):
        return self.verifier.verify(value)

    def tostr(self):
        return "name=%s;type=%s;nullable=%s;default=%s" % (self.name, self.type.tostr(), str(self.nullable), self.default.tostr())

    def fromstr(self, str):
        field_regex = re.compile(r'^\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*type\s*=\s*(?P<type>.+)\s*;\s*nullable\s*=\s*(?P<nullable>[\w]+)\s*;\s*default\s*=\s*(?P<default>.+)\s*$')
        mobj = field_regex.match(str)
        if mobj:
            sname, stype, snullable, sdefault = mobj.group('name', 'type', 'nullable', 'default')
            self.name, self.type, self.nullable, self.default = sname, Type().fromstr(stype), str2bool(snullable), Value().fromstr(sdefault)
            return self


if __name__ == "__main__":
    field1 = Field("id", Int(), False, AutoIncValue())
    field2 = Field("code", String(32), False)
    field3 = Field("name", String(32), True, StringValue('name'))
    field4 = Field("valid", Boolean(), True, BooleanValue(True))
    field5 = Field("create_time", BigInt(), True)

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

