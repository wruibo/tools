'''
    table for storage
'''
from storage.ckey import *
from storage.ctype import *
from storage.cvalue import *
from storage.cfield import *
from storage.cverifier import *


class Table:
    '''
        base table class for storage
    '''
    def __init__(self, name=None):
        self.name = name
        self.fields = []
        self.keys = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name==other.name and self.fields == other.fields
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def field(self, name, type, default=DefaultNull(), verifier=DefaultVerifier()):
        self.fields.append(Field(name, type, default, verifier))

    def key(self, keycls, name, *fields):
        self.keys.append(keycls(name, *fields))

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
        sql_table = "create table %s\n(\n%s\n\n%s\n);" % (self.name, sql_fields, sql_keys)

        return sql_table

    def fromsql(self, sql):
        '''
            create table from sql
        :param sql:
        :return:
        '''
        regex_fields = re.compile(r"(`\w+`\s+\w+(\([,\d\s]+\))?([^,\)]+)?)[,|\)]", re.IGNORECASE)

        #regex_keys = re.compile(r"(\w+\s+)?key\s*(`\w+`)?\s*\([^\(\)]+\)[\s,|\)]", re.IGNORECASE)

        regex_keys = re.compile(r'((unique|primary)?'
                               r'key'
                               r'(`)?'
                               r'[\w_]+'
                               r'(`)?'
                               r'\('
                               r'[`\w,\s]+'
                               r'\))',
                               re.IGNORECASE)

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
                    else:
                        pass
                else:
                    pass
        return self


class DemoTable(Table):
    def __init__(self, name="tb_demo"):
        Table.__init__(self, name)

        self.field("id", Int(), AutoIncValue())
        self.field("code", String(32))
        self.field("name", String(32), StringValue("abc"))
        self.field("valid", Boolean())
        self.field("create_time", BigInt())

        self.key(PrimaryKey, "pk_id", "id")
        self.key(NormalKey, "normal_key", "name", "code")
        self.key(UniqueKey, "unique_key", "code", "valid")


if __name__ == "__main__":
    table = DemoTable()

    print table.tosql()

    str1 = table.tostr()
    print str1

    print DemoTable().fromstr(str1).tostr()

    sql = "CREATE TABLE `tb_demo` (\
              `id` int(11) NOT NULL AUTO_INCREMENT,\
              `code` varchar(32) NOT NULL DEFAULT 'abc',\
              `name` varchar(32) DEFAULT NULL,\
              `valid` tinyint(1) NOT NULL DEFAULT 0,\
              `create_time` bigint(20) DEFAULT NULL,\
                  PRIMARY KEY (`id`),\
                  UNIQUE KEY `unique_key` (`code`,`valid`),\
                  UNIQUE KEY `unique_index` (`code`,`valid`),\
                  KEY `normal_key` (`name`,`code`),\
                  KEY `normal_index` (`name`,`code`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8"

    t = Table().fromsql(sql)
    print t