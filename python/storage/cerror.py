'''
    error for storage
'''


class DBError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args, **kwargs)

DBConnectionError = DBError

if __name__ == "__main__":
    error = DBConnectionError("error!!")
    print(error)