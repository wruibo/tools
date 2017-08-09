"""
    cache base class/functions
"""
import time


class Cache:
    """
        cache base class
    """
    def save(self, key, content, wantold=False, encoding='utf-8'):
        """
            save text content with key into cache
        :param key: str, key for content
        :param content: str, content for cache
        :param wantold: bool, return old content if want
        :param encoding: str, encoding of content
        :return: str, old content or None
        """
        pass

    def take(self, key, maxage=None, encoding='utf-8'):
        """
            take text content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :param encoding: str, encoding of content
        :return: str, content, or None
        """
        pass

    def saveb(self, key, content, wantold=False):
        """
            save binary content with key into cache
        :param key: str, key for content
        :param content: bytes, content for cache
        :param wantold: bool, return old content if want
        :return: bytes, old content or None
        """
        pass

    def takeb(self, key, maxage=None):
        """
            take binary content with key from cache
        :param key: str, key for content
        :param maxage: int, max age for cache in seconds
        :return: bytes, content, or None
        """
        pass

    def packctm(self, content):
        """
            pack source content and create unix timestamp to packed content
        :param content: str or bytes, data to pack
        :param encoding: str, encoding of content
        :return: str or bytes, save as input source content
        """
        currtm = str(int(time.time())).zfill(16)

        if isinstance(content, str):
            return currtm+content

        if isinstance(content, bytes):
            return currtm.encode()+content

        raise "pack content error: input content type must be str or bytes."

    def unpackctm(self, data):
        """
            unpack source content and create timestamp from packed content
        :param data: str or bytes, data to unpack
        :param encoding: str, encoding of content
        :return: str or bytes, save as input source content
        """
        if isinstance(data, str):
            return int(data[0:16]), data[16:]

        if isinstance(data, bytes):
            return int(data[0:16].decode()), data[16:]

        raise "unpack data error: input data type must be str or bytes."
