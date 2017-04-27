'''
    field for define table
'''
from utility.ccast import *

from storage.ctype import Type
from storage.cvalue import Value
from storage.cverifier import Verifier


class Field:
    def __init__(self, name, type, nullable=True, default=Value.Null(), verifier=Verifier.DefaultVerifier()):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.default = default
        self.verifier = verifier

    def verify(self, value):
        return self.verifier.verify(value)

    def tostr(self):
        return "name=%s;type=%s;nullable=%s;default=%s" % (self.name, self.type.tostr(), str(self.nullable), self.default.tostr())

    @staticmethod
    def fromstr(str):
        import re
        field_regex = re.compile(r'^\s*name\s*=\s*(?P<name>[\w]+)\s*;\s*type\s*=\s*(?P<type>.+)\s*;\s*nullable\s*=\s*(?P<nullable>[\w]+)\s*;\s*default\s*=\s*(?P<default>.+)\s*$')
        mobj = field_regex.match(str)
        if mobj:
            sname, stype, snullable, sdefault = mobj.group('name', 'type', 'nullable', 'default')

            return Field(sname, Type.fromstr(stype), str2bool(snullable), Value.fromstr(sdefault))


if __name__ == "__main__":
    field1 = Field("id", Type.Int(), False, Value.AutoInc())
    field2 = Field("code", Type.String(32), False)
    field3 = Field("name", Type.String(32), True, Value.String('name'))
    field4 = Field("valid", Type.Boolean(), True, Value.Boolean(True))
    field5 = Field("create_time", Type.BigInt(), True)

    print field1.tostr()
    print field2.tostr()
    print field3.tostr()
    print field4.tostr()
    print field5.tostr()

    print Field.fromstr(field1.tostr()).tostr()
    print Field.fromstr(field2.tostr()).tostr()
    print Field.fromstr(field3.tostr()).tostr()
    print Field.fromstr(field4.tostr()).tostr()
    print Field.fromstr(field5.tostr()).tostr()

