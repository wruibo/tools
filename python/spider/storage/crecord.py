
class MetaRecord(type):
    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kargs):
        pass


class Record(dict):
    __metaclass__ = MetaRecord

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self[key] = kwargs.get(key)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class DemoRecord(Record):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.code = kwargs.get("code", None)
        self.name = kwargs.get("name", None)
        self.valid = kwargs.get("valid", None)
        self.create_time = kwargs.get("create_time", None)

    @staticmethod
    def random_records(num):
        import time

        records = []
        for i in range(1, num+1):
            records.append(DemoRecord(id=i, code="code%d" % i, name="name%d" % i, valid=True, create_time=time.time()))
        return records

if __name__ == "__main__":
    record = DemoRecord(id=10, code="0010", name="demo")
    print record.id
    print record['id']
    print record.name
    print record['name']
    print DemoRecord.random_records(10)

