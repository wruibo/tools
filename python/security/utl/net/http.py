"""
    http based remote data access
"""
import requests as _requests

from . import data as _data
from .. import cache as _cache
from .. import hash as _hash


class _Client:
    _http_use_cache = True

    """
        http class for remote data access
    """
    def __init__(self, url, params=None, data=None, json=None, **kwargs):
        """
            initialize http access object with url
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`
        :param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        self._url = url
        self._params = params
        self._data = data
        self._json = json
        self._kwargs = kwargs

        self._key = _Client.key(url, params, data)

    @staticmethod
    def cache(on=None):
        """
            set http cache flag
        :param on:
        :return:
        """
        if on is not None:
            _Client._http_use_cache = on
        else:
            return _Client._http_use_cache

    @staticmethod
    def key(url, params, data):
        """
            generate unique key for current http request
        :param url:
        :param params:
        :param data:
        :return:
        """
        strs = []

        # add url
        if url is not None:
            strs.append(url)

        # add parameters
        if isinstance(params, dict):
            for key, value in params.items():
                strs.append("%s=%s" % (str(key), str(value)))

        # add data
        if isinstance(data, dict):
            for key, value in data.items():
                strs.append("%s=%s" % (str(key), str(value)))

        # generate key
        return _hash.sha1("".join(strs).encode())

    def get(self, maxage=None):
        """
            get byte data and wrap to dao object by using get method
        :return: dao, data access object
        """
        # get from cache first
        if _Client.cache():
            content = _cache.takeb(self._key, maxage)
            if content is not None: return _data.Data(content)

        # request content from remote url
        resp = _requests.get(self._url, self._params, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.content

            # cache data
            if _Client.cache():
                _cache.saveb(self._key, content)

            # return dao object
            return _data.Data(content)
        else:
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

    def post(self, maxage=None):
        """
            get byte data and wrap to dao object by using post method
        :return: dao, data access object
        """
        # get from cache first
        if _Client.cache():
            content = _cache.takeb(self._key, maxage)
            if content is not None: return _data.Data(content)

        # request content from remote url
        resp = _requests.post(self._url, self._data, self._json, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.content

            # cache data
            if _Client.cache():
                _cache.saveb(self._key, content)

            # return dao object
            return _data.Data(content)
        else:
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

    def xget(self, maxage=None):
        """
            get byte data and wrap to dao object by using get method
        :return: dao, data access object
        """
        # get from cache first
        if _Client.cache():
            content = _cache.take(self._key, maxage)
            if content is not None: return _data.Data(content)

        # request content from remote url
        resp = _requests.get(self._url, self._params, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.text

            # cache data
            if _Client.cache():
                _cache.save(self._key, content)

            # return dao object
            return _data.Data(content)
        else:
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

    def xpost(self, maxage=None):
        """
            get byte data and wrap to dao object by using post method
        :return: dao, data access object
        """
        # get from cache first
        if _Client.cache():
            content = _cache.take(self._key, maxage)
            if content is not None: return _data.Data(content)

        # request content from remote url
        resp = _requests.post(self._url, self._data, self._json, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.text

            # cache data
            if _Client.cache():
                _cache.save(self._key, content)

            # return dao object
            return _data.Data(content)
        else:
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))


client = _Client
