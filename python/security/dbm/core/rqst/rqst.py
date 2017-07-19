"""
    requests wrapper with cache function
"""
import dbm, utl, json, requests, xml.dom.minidom


#cache flag for request
_use_cache = True


def cache(usecache=None):
    """
        set cache flag
    :param usecache: bool, True-cache will be used, False-cache will be closed
    :return: bool, when @usecache is None return _cache
    """
    global _use_cache
    if usecache is None:
        return _use_cache
    else:
        _use_cache = usecache



def gettxt(url, params=None, **kwargs):
    """
        get text content from url
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    # use cache content if exists
    if cache():
        content = dbm.core.cache.take(utl.hash.sha1(url.encode()))
        if content is not None: return content

    # request content from remote url
    content = requests.get(url, params, **kwargs).text

    # cache response content to cache
    if cache():
        dbm.core.cache.save(utl.hash.sha1(url.encode()), content)

    # return json data object
    return content

def getxml(url, params=None, **kwargs):
    """
        get xml content from url
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    # use cache content if exists
    if cache():
        content = dbm.core.cache.take(utl.hash.sha1(url.encode()))
        if content is not None:
            return xml.dom.minidom.parseString(content)

    # request content from remote url
    content = requests.get(url, params, **kwargs).text

    # parse content use xml dom
    dom = xml.dom.minidom.parseString(content)

    # cache response content to cache
    if cache():
        dbm.core.cache.save(utl.hash.sha1(url.encode()), content)

    # return json data object
    return dom


def getjson(url, params=None, **kwargs):
    """
        get json content from url
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    # use cache content if exists
    if cache():
        content = dbm.core.cache.take(utl.hash.sha1(url.encode()))
        if content is not None:
            return json.loads(content)

    # request content from remote url
    content = requests.get(url, params, **kwargs).text

    # parse content use json
    json_data = json.loads(content)

    # cache response content to cache
    if cache():
        dbm.core.cache.save(utl.hash.sha1(url.encode()), content)

    # return json data object
    return json_data

