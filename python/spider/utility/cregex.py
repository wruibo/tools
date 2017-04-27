'''
    regex tools
'''
import re

class regex:
    def __init__(self):
        pass

    @staticmethod
    def match(pattern, string, default='', flags=0):
        mobj = re.match(pattern, string, flags)
        if mobj is None:
            return None
        return mobj.groups(default)

    @staticmethod
    def search(pattern, string, default='', flags=0):
        mobj = re.search(pattern, string, flags)
        if mobj is None:
            return None
        return mobj.groups(default)

    @staticmethod
    def findone(pattern, string, flags=0):
        pass

    @staticmethod
    def findall(pattern, string, flags=0):
        mstrs = re.findall(pattern, string, flags)
        return mstrs


if __name__ == "__main__":
    re.fi