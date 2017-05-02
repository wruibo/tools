'''
    string tools
'''


def strips(strs, chars=None):
    if isinstance(strs, list) or isinstance(strs, tuple):
        stripeds = []
        for str in strs:
            stripeds.append(str.strip(chars))
        return stripeds
    else:
        return strs.strip(chars)


def quote(str, q="'"):
    return "%s%s%s" % (q, str, q)


def unquote(str):
    return str.strip("'\"")

if __name__ == "__main__":
    print quote("123", '"')
    print unquote("\'a\'")