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

        self._key = http.key(url, params, data)

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
        return utl.hash.sha1("".join(strs).encode())

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
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

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
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

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
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

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
        resp = requests.post(self._url, self._data, self._json, **self._kwargs)

        if resp.ok:
            # get content
            content = resp.text

            # cache data
            if http.cache():
                dbm.core.cache.save(self._key, content)

            # return dao object
            return dbm.core.rda.dao(content)
        else:
            raise Exception("request failed for %s %s, url: %s" % (resp.status_code, resp.reason, self._url))

