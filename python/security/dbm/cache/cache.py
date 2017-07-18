"""
    cache
"""
import os


# default cache directory
_cachedir = "."


def setdir(cachedir):
    """
        change cache directory
    :param cachedir: str, new cache directory path
    :return:
    """
    _cachedir = cachedir


def save(key, content):
    """
        save content with key into cache
    :param key: str, key for content
    :param content:
    :return: old content or None
    """
    oldcontent = None

    cachefile = _cachedir+"/"+key

    if os.path.exists(cachefile) and os.path.isfile(cachefile):
        with open(cachefile, "r") as f:
            oldcontent = f.read()

    with open(cachefile, "w") as f:
        f.write(content)

    return oldcontent


def take(key):
    """
        take content with key from cache
    :param key: str, key for content
    :return: content, or None
    """
    content = None

    cachefile = _cachedir + "/" + key

    if os.path.exists(cachefile) and os.path.isfile(cachefile):
        with open(cachefile, "r") as f:
            content = f.read()

    return content