'''
    error for store
'''


class DBError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args, **kwargs)

DBConnectionError = DBError
DBStorageNotSpecifiedError = DBError


def check_none(obj, error):
    if obj is None:
        raise error

if __name__ == "__main__":
    error = DBConnectionError("error!!")
    print(error)