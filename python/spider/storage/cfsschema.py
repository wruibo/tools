'''
    schema for file system based database
'''


class FSSchema:
    def __init__(self):
        pass

    @staticmethod
    def load(schema_file):
        '''
            load schema from schema file
        :param file:
        :return:
        '''
        with open(schema_file, 'r') as fschema:
            str = fschema.read()
            return FSSchema.str2schema(str)

    @staticmethod
    def save(schema_file, schema):
        '''
            save schema to schema file
        :param schema_file:
        :param schema:
        :return:
        '''
        str = FSSchema.schema2str(schema)

        with open(schema_file, 'w') as fschema:
            fschema.write(str)

        return None

    @staticmethod
    def schema2str(schema):
        '''
            translate schema to string
        :param schema:
        :return:
        '''
        return schema.tostr()

    @staticmethod
    def str2schema(str):
        '''
            translate string to schema
        :param str:
        :return:
        '''
        #
        return Schema.fromstr(str)


if __name__ == "__main__":
    from storage.ckey import *
    from storage.ctype import *
    from storage.cvalue import *
    from storage.cindex import *
    from storage.cschema import Schema

    schema = Schema()
    schema.field("id", Type.Int(), False, Value.AutoInc())
    schema.field("code", Type.String(32), False, None)
    schema.field("name", Type.String(32), True, None)
    schema.field("valid", Type.Boolean(), True, None)
    schema.field("create_time", Type.BigInt(), True, None)

    schema.key(Key.PrimaryKey, "pk_id", "id")
    schema.key(Key.NormalKey, "normal_key", "name")
    schema.key(Key.UniqueKey, "unique_key", "code")

    schema.index(Index.NormalIndex, "normal_index", "name")
    schema.index(Index.UniqueIndex, "unique_index", "code")

    str = FSSchema.schema2str(schema)
    print str






