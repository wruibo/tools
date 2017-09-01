"""
    cache for data
"""


class vendor:
    @staticmethod
    def file(name='default', dirpath=None):
        """
            open a new file cache
        :param name: str, name of the cache
        :param dirpath: str or None, cache directory path
        :return: obj, file cache
        """
        from . import filec
        return filec.FileCache(name, dirpath)

    @staticmethod
    def gnudbm(name='default', dirpath=None):
        """
            open a new gnu dbm cache
        :param name: str, name of the cache
        :param dirpath: str or None, cache directory path
        :return: obj, file cache
        """
        from .import gnuc
        return gnuc.GNUDBMCache(name, dirpath)


#global default cache object
__default_cache = vendor.file()


def default(cache=None):
    """
        change the default cache type
    :param cache: object, FileCache or GNUDBMCache object
    :return:
    """
    global __default_cache
    if cache is not None:
        __default_cache = cache
    else:
        return __default_cache


def save(key, content, wantold=False, encoding='utf-8'):
    """
        save text content with key into cache
    :param key: str, key for content
    :param content: str, content for cache
    :param wantold: bool, return old content if want
    :param encoding: str, encoding of content
    :return: str, old content or None
    """
    return default().save(key, content, wantold, encoding)


def take(key, maxage=None, encoding='utf-8'):
    """
        take text content with key from cache
    :param key: str, key for content
    :param maxage: int, max age for cache in seconds
    :param encoding: str, encoding of content
    :return: str, content, or None
    """
    return default().take(key, maxage, encoding)


def saveb(key, content, wantold=False):
    """
        save binary content with key into cache
    :param key: str, key for content
    :param content: bytes, content for cache
    :param wantold: bool, return old content if want
    :return: bytes, old content or None
    """
    return default().saveb(key, content, wantold)


def takeb(key, maxage=None):
    """
        take binary content with key from cache
    :param key: str, key for content
    :param maxage: int, max age for cache in seconds
    :return: bytes, content, or None
    """
    return default().takeb(key, maxage)

