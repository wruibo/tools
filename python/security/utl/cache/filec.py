"""
    file cache: cache data using file system
"""
import os, time

from . import base
from .. import file

class FileCache(base.Cache):
    """
        file cache class
    """
    # cache dataware house, default cache directory and cache name
    _default_cache_dir = file.tempdir() + "/dbmcache"
    _default_cache_name = "default"

    def __init__(self, name=_default_cache_name, dirpath=_default_cache_dir):
        """
            initialize file cache with cache directory path
        :param name: str or None, cache name
        :param dirpath: str or None, cache directory path
        """
        if name is None: name = self._default_cache_name
        if dirpath is None: dirpath = self._default_cache_dir

        cachedir = dirpath+"/"+name
        if not os.path.exists(cachedir):
            os.makedirs(cachedir)

        self._cachedir = cachedir

    def _cache_file(self, key):
        """
            get cache file path by input key
        :param key: str, key for cache content
        :return: str, cache file path of key
        """
        return self._cachedir + "/" + key

    def cachedir(self, dirpath=None):
        """
            get or set the cache file directory path
        :param dirpath: str or None, cache file directory path
        :return: str or None
        """
        if dirpath is not None:
            self._cachedir = dirpath
        else:
            return self._cachedir

    def save(self, key, content, wantold=False, encoding='utf-8'):
        """
            save text content with key into cache
        :param key: str, key for content
        :param content: str, content for cache
        :param wantold: bool, return old content if want
        :param encoding: str, encoding of content
        :return: str, old content or None
        """
        oldcontent = None

        cachefile = self._cache_file(key)

        # get old content if set the wantold flag to True
        if os.path.exists(cachefile) and os.path.isfile(cachefile) and wantold:
            with open(cachefile, "r", encoding=encoding) as f:
                oldcontent = f.read()

        # write the new cache content
        with open(cachefile, "w", encoding=encoding) as f:
            f.write(content)

        return oldcontent

    def take(self, key, maxage=None, encoding='utf-8'):
        """
            take text content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :param encoding: str, encoding of content
        :return: str, content, or None
        """
        cachefile = self._cache_file(key)

        if os.path.exists(cachefile) and os.path.isfile(cachefile):
            if maxage is not None:
                if int(time.time()) - os.path.getctime(cachefile) > maxage:
                    return None

            with open(cachefile, "r", encoding=encoding) as f:
                content = f.read()
                return content

        return None

    def saveb(self, key, content, wantold=False):
        """
            save binary content with key into cache
        :param key: str, key for content
        :param content: bytes, content for cache
        :param wantold: bool, return old content if want
        :return: bytes, old content or None
        """
        oldcontent = None

        cachefile = self._cache_file(key)

        # get old content if set the wantold flag to True
        if os.path.exists(cachefile) and os.path.isfile(cachefile) and wantold:
            with open(cachefile, "rb") as f:
                oldcontent = f.read()

        # write the new cache content
        with open(cachefile, "wb") as f:
            f.write(content)

        return oldcontent

    def takeb(self, key, maxage=None):
        """
            take binary content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :return: bytes, content, or None
        """
        cachefile = self._cache_file(key)

        if os.path.exists(cachefile) and os.path.isfile(cachefile):
            if maxage is not None:
                if int(time.time()) - os.path.getctime(cachefile) > maxage:
                    return None

            with open(cachefile, "rb") as f:
                content = f.read()
                return content

        return None

if __name__ == "__main__":
    cache = FileCache("cfq")
    cache.save('abc', "abc")
    cache.saveb('abcd', b"abcd")
    print(cache.take('abc'))
    print(cache.takeb('abcd'))
