'''
    schema for table creation
'''
from storage.ckey import Key
from storage.ctype import Type
from storage.cvalue import Value
from storage.cindex import Index
from storage.cfield import Field
from storage.cverifier import Verifier


class Schema:
    def __init__(self, name=None):
        self.name = name

        self.fields = []
        self.keys = []
        self.indexs = []

    def __eq__(self, other):
        return self.name==other.name and self.fields == other.fields and self.keys==other.keys and self.indexs==other.indexs

    def field(self, name, type, nullable=True, default=Value.Null(), verifier=Verifier.DefaultVerifier()):
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
        import re
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
                        self.fields.append(Field.fromstr(line))
                    elif section == 'keys':
                        self.keys.append(Key.fromstr(line))
                    elif section == 'indexs':
                        self.indexs.append(Index.fromstr(line))
                    else:
                        pass
                else:
                    pass
        return self


if __name__ == "__main__":
    from storage.ctype import Type
    from storage.ckey import Key
    from storage.cindex import Index
    from storage.cvalue import Value

    schema = Schema("tb_demo")
    schema.field("id", Type.Int(), False, Value.AutoInc())
    schema.field("code", Type.String(32), False)
    schema.field("name", Type.String(32), True)
    schema.field("valid", Type.Boolean(), True)
    schema.field("create_time", Type.BigInt(), True)

    schema.key(Key.PrimaryKey, "pk_id", "id")
    schema.key(Key.NormalKey, "normal_key", "name","code")
    schema.key(Key.UniqueKey, "unique_key", "code", "valid")

    schema.index(Index.NormalIndex, "normal_index", "name", "code")
    schema.index(Index.UniqueIndex, "unique_index", "code", "valid")

    str1 = schema.tostr()
    print str1

    schema = Schema()
    print schema.fromstr(str1).tostr()
