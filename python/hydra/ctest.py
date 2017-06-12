class TestProperty:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value


def log(func):
    def aa(*args, **kwargs):
        print("log")
        func(*args, **kwargs)
    return aa

@log
def now():
    import time
    print(time.time())

def fn(self, name="ena"):
    print("abc")

Hello = type('Hello', (object,), dict(hello=fn, hello1=fn))


class QueIter:
    def __init__(self, count):
        self.count = count

    def __next__(self):
        self.count -= 1
        if self.count == 0:
            raise StopIteration
        return self.count

class Que:
    def __init__(self):
        pass

    def __iter__(self):
        return QueIter(10)



if __name__ == "__main__":
    import re

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

    regex_keys = re.compile(r'('
                            r'(unique\s+|primary\s+)?'
                            r'key\s*'
                            r'(`?[\w_]+`?\s*)?'
                            r'\([^\(\)]+\)'
                            r')',
                            re.IGNORECASE)
    mobjs = regex_keys.findall(sql)
    for mobj in mobjs:
        print(mobj[0])

    print("\n\n")
    regex_fields =  re.compile(r'('
                               r'`[\w_]+`\s+'
                               r'\w+'
                               r'(\([^\(\)]+\))?\s+'
                               r'[^,]*'
                               r')',
                               re.IGNORECASE)
    mobjs = regex_fields.findall(sql)
    for mobj in mobjs:
        print(mobj[0])