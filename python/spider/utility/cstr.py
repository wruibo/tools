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


def quotes(s, q="'"):
    if isinstance(s, str):
        return "%s%s%s" % (q, s, q)
    else:
        strs = []
        for ss in s:
            strs.append("%s%s%s" % (q, ss, q))
        return strs

def unquotes(s, q="'\""):
    if isinstance(s, str):
        return s.strip(q)
    else:
        strs = []
        for ss in s:
            strs.append(ss.strip(q))
        return strs


if __name__ == "__main__":
    print quotes(("123","345"), '"')
    print unquotes("\'a\'")