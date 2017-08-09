"""
    gnu dbm cache: cache data using gun dbm library
"""
import os, utl, time
import _gdbm
from dbm.core.cache.base import Cache


class GNUDBMCache(Cache):
    """
        gun dbm cache class
    """
    # cache dataware house, default cache directory
    _default_cache_dir = utl.fd.tempdir() + "/dbmcache"

    def __init__(self, name):
        """
            initialize file cache with cache file path
        :param name: str, cache name
        """
        cachedir = self._default_cache_dir
        if not os.path.exists(cachedir):
            os.makedirs(cachedir)

        cachefile = self._default_cache_dir+"/"+name
        self._dbm = _gdbm.open(cachefile, 'c')

    def save(self, key, content, wantold=False, encoding='utf-8'):
        """
            save text content with key into cache
        :param key: str, key for content
        :param content: str, content for cache
        :return: str, old content or None
        """
        # get old content if set the wantold flag to True
        oldcontent = self._dbm.get(key)

        # pack content with create timestamp
        data = self.packctm(content)

        # write the new cache content
        self._dbm[key] = data.encode(encoding)

        return oldcontent

    def take(self, key, maxage=None, encoding='utf-8'):
        """
            take text content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :return: str, content, or None
        """
        # get data from cache by key
        data = self._dbm.get(key)
        if data is None:
            return

        # unpack data, and check cache's expire time
        ctime, content = self.unpackctm(data)
        if maxage is not None and int(time.time()) - ctime > maxage:
            return

        return content.decode(encoding)

    def saveb(self, key, content, wantold=False):
        """
            save binary content with key into cache
        :param key: str, key for content
        :param content: bytes, content for cache
        :return: bytes, old content or None
        """
        # get old content if set the wantold flag to True
        oldcontent = self._dbm.get(key)

        # pack content with create timestamp
        data = self.packctm(content)

        # write the new cache content
        self._dbm[key] = data

        return oldcontent

    def takeb(self, key, maxage=None):
        """
            take binary content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :return: bytes, content, or None
        """
        # get data from cache by key
        data = self._dbm.get(key)
        if data is None:
            return

        # unpack data, and check cache's expire time
        ctime, content = self.unpackctm(data)
        if maxage is not None and int(time.time()) - ctime > maxage:
            return

        return content


if __name__ == "__main__":
    cache = GNUDBMCache('smw')
    #cache.save('abc', "abc")
    #cache.saveb('abcd', b"abcd")
    print(cache.take('abc', 300))
    print(cache.takeb('abcd', 190))
