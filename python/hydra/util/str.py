'''
    string tools
'''


def strips(ss, chars=None):
    '''
        strip @chars in string
    :param ss:
    :param chars:
    :return:
    '''
    if isinstance(ss, list) or isinstance(ss, tuple):
        stripeds = []
        for s in ss:
            stripeds.append(s.strip(chars))
        return stripeds
    else:
        return ss.strip(chars)

def escapes(ss, chars="'\""):
    '''
        escape @chars in string @ss or string list(or tupple) @ss
    :param s:
    :param chars:
    :return:
    '''
    if isinstance(ss, str):
        for ch in chars:
            ss = ss.replace(ch, "%" + str(hex(ord(ch))))
        return ss
    elif isinstance(ss, list) or isinstance(ss, tuple):
        slst = []
        for s in ss:
            slst.append(escapes(s, chars))
        return slst
    else:
        return ss


def unescapes(ss, chars="'\""):
    '''
        unescape @chars in string @ss or string list(or tupple) @ss
    :param ss:
    :param chars:
    :return:
    '''
    if isinstance(ss, str):
        for ch in chars:
            ss = ss.replace("%" + str(hex(ord(ch))), ch)
        return ss
    elif isinstance(ss, list) or isinstance(ss, tuple):
        slst = []
        for s in ss:
            slst.append(escapes(s, chars))
        return slst
    else:
        return ss

def quotes(ss, q="'"):
    '''
        quote string @ss or string list(or tuple) @ss with quote @q
    :param ss:
    :param q:
    :return:
    '''
    if isinstance(ss, str):
        return "%s%s%s" % (q, ss, q)
    elif isinstance(ss, list) or isinstance(ss, tuple):
        slst = []
        for s in ss:
            slst.append(quotes(s, q))
        return slst
    else:
        return ss

def unquotes(ss, q="'\""):
    '''
        unquote string @str or string list(or tuple) @ss with quote @q
    :param ss:
    :param q:
    :return:
    '''
    if isinstance(ss, str):
        return ss.strip(q)
    elif isinstance(ss, list) or isinstance(ss, tuple):
        slst = []
        for s in ss:
            slst.append(unquotes(s, q))
        return slst
    else:
        return ss


if __name__ == "__main__":
    print quotes(("123","345"), '"')
    print unquotes("\'a\'")