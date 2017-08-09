"""
    cache for data
"""
__all__ = ["cache"]

class file:
    @staticmethod
    def open(name='default'):
        from dbm.core.cache.filec import FileCache
        return FileCache(name)

class gnudbm:
    @staticmethod
    def open(name='default'):
        from dbm.core.cache.gnuc import GNUDBMCache
        return GNUDBMCache(name)


_default_cache = file.open()


def default(cache):
    """
        change the default cache type
    :param cache: object, FileCache or GNUDBMCache object
    :return:
    """
    global _default_cache
    _default_cache = cache


def save(key, content, wantold=False, encoding='utf-8'):
    """
        save text content with key into cache
    :param key: str, key for content
    :param content: str, content for cache
    :param wantold: bool, return old content if want
    :param encoding: str, encoding of content
    :return: str, old content or None
    """
    return _default_cache.save(key, content, wantold, encoding)


def take(key, maxage=None, encoding='utf-8'):
    """
        take text content with key from cache
    :param key: str, key for content
    :param maxage: int, max age for cache in seconds
    :param encoding: str, encoding of content
    :return: str, content, or None
    """
    return _default_cache.take(key, maxage, encoding)


def saveb(key, content, wantold=False):
    """
        save binary content with key into cache
    :param key: str, key for content
    :param content: bytes, content for cache
    :param wantold: bool, return old content if want
    :return: bytes, old content or None
    """
    return _default_cache.saveb(key, content, wantold)


def takeb(key, maxage=None):
    """
        take binary content with key from cache
    :param key: str, key for content
    :param maxage: int, max age for cache in seconds
    :return: bytes, content, or None
    """
    return _default_cache.takeb(key, maxage)

if __name__ == "__main__":
    save('a', 'a123')
    print(take('a'))

    saveb('b', b'b123')
    print(takeb('b'))

    file.open('cfq').save('c', 'c123')
    print(file.open('cfq').take('c'))