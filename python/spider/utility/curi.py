'''
    URI tools
'''
import re


class curi:
    def __init__(self):
        pass

    @staticmethod
    def parse(uri):
        pattern = r"^(\w*):[/]*([^/]+)(.*)"
        matchobj = re.match(pattern, uri.strip(), re.IGNORECASE)
        if matchobj is not None:
            return matchobj.groups()
        return None

    @staticmethod
    def protocol(uri):
        pattern = r"^(\w+):"
        matchobj = re.match(pattern, uri.strip(), re.IGNORECASE)
        if matchobj is not None:
            return matchobj.group(1)
        return None

    @staticmethod
    def host(uri):
        pattern = r"\w+://([^/]+)"
        matchobj = re.match(pattern, uri.strip(), re.IGNORECASE)
        if matchobj is not None:
            return matchobj.group(1)
        return None

    @staticmethod
    def path(uri):
        pattern = r"\w+://[^/]+(.*)"
        matchobj = re.match(pattern, uri.strip(), re.IGNORECASE)
        if matchobj is not None:
            return matchobj.group(1)
        return None

    @staticmethod
    def is_remote(uri):
        '''
            detect whether @path is remote url, like: http://..., ftp://..., file://...
        :param uri: string, path to detect
        :return: boolean
        '''
        pattern = r'^\w+://.*'
        return re.match(pattern, uri, re.IGNORECASE) is not None

    @staticmethod
    def is_relative(uri):
        return not curi.is_remote(uri)

if __name__ == "__main__":
    url = "http://www.dns.com/path/file"
    #url = "/path1/path2/file"
    #url = "../path/file"
    #url = "mailto:abc@abc.com"

    print curi.parse(url)
    print curi.protocol(url)
    print curi.host(url)
    print curi.path(url)