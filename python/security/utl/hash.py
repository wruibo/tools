"""
    hash method
"""
import hashlib


def md5(str):
    '''
        compute md5 of @str
    :return: string
    '''
    m = hashlib.md5()
    m.update(str)

    return m.hexdigest()



def sha1(str):
    '''
        compute sha1 of @str
    :return: string
    '''
    h = hashlib.sha1()
    h.update(str)

    return h.hexdigest()