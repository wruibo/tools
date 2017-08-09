"""
    http based remote data access
"""
import utl, dbm, requests

_http_use_cache = True

class http:
    """
        http class for remote data access
    """
    def __init__(self, url, params=None, data=None, json=None, **kwargs):
        """
            initialize http access object with url
        :param url:
        :param params:
        :param data:
        :param json:
        :param kwargs:
        """
        self._url = url
        self._key = utl.hash.sha1(url.encode())
        self._params = params
        self._data = data
        self._json = json
        self._kwargs = kwargs

    @staticmethod
    def cache(on=None):
        """
            set http cache flag
        :param on:
        :return:
        """
        global _http_use_cache
        if on is not None:
            _http_use_cache = on
        else:
            return _http_use_cache

    def get(self, maxage=None):
        """
            get byte data and wrap to dao object by using get method
        :return: dao, data access object
        """
        # get from cache first
        if http.cache():
            content = dbm.core.cache.takeb(self._key, maxage)
            if content is not None: return dbm.core.rda.dao(content)

        # request content from remote url
        resp = requests.get(self._url, self._params, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.content

            # cache data
            if http.cache():
                dbm.core.cache.saveb(self._key, content)

            # return dao object
            return dbm.core.rda.dao(content)
        else:
            raise "request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url)

    def post(self, maxage=None):
        """
            get byte data and wrap to dao object by using post method
        :return: dao, data access object
        """
        # get from cache first
        if http.cache():
            content = dbm.core.cache.takeb(self._key, maxage)
            if content is not None: return dbm.core.rda.dao(content)

        # request content from remote url
        resp = requests.post(self._url, self._data, self._json, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.content

            # cache data
            if http.cache():
                dbm.core.cache.saveb(self._key, content)

            # return dao object
            return dbm.core.rda.dao(content)
        else:
            raise "request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url)

    def xget(self, maxage=None):
        """
            get byte data and wrap to dao object by using get method
        :return: dao, data access object
        """
        # get from cache first
        if http.cache():
            content = dbm.core.cache.take(self._key, maxage)
            if content is not None: return dbm.core.rda.dao(content)

        # request content from remote url
        resp = requests.get(self._url, self._params, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.text

            # cache data
            if http.cache():
                dbm.core.cache.save(self._key, content)

            # return dao object
            return dbm.core.rda.dao(content)
        else:
            raise "request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url)

    def xpost(self, maxage=None):
        """
            get byte data and wrap to dao object by using post method
        :return: dao, data access object
        """
        # get from cache first
        if http.cache():
            content = dbm.core.cache.take(self._key, maxage)
            if content is not None: return dbm.core.rda.dao(content)

        # request content from remote url
        resp = requests.post(self._url, self._data, self._json, **self._kwargs).text

        if resp.ok:
            # get content
            content = resp.text

            # cache data
            if http.cache():
                dbm.core.cache.save(self._key, content)

            # return dao object
            return dbm.core.rda.dao(content)
        else:
            raise "request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url)

