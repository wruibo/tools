'''
    value cast between types
'''

ValueCastError = Exception

def isnone(s):
    '''
        test if input string is None value
    :param s:
    :return:
    '''
    s = s.strip().strip("'\"").lower()
    if s == 'none' or s == 'null':
        return True
    return False

def none2str(none):
    '''
        None value to str
    :param none:
    :return:
    '''
    return str(none)

def str2none(s):
    '''
        string value to none
    :param s:
    :return:
    '''
    if not isnone(s):
        raise ValueCastError("input string value is %s, expect none/None/...." % s)

    return None

def isbool(s):
    '''
        test if input string is bool value
    :param s:
    :return:
    '''
    s = s.strip().strip('"\'').lower()
    if s == 'true' or s == 'false':
        return True
    return False

def bool2str(b):
    '''
        boolean value to string:
        True->'true'
        False->'false'
    :param b:
    :return:
    '''
    if not isinstance(b, bool):
        raise ValueCastError("input value type is %s, expect bool." % b.__class__.__name__)
    return str(b)

def str2bool(s):
    '''
        boolean string to boolean:
        'true','True', 'TRUE',...->True
        'false', 'False', 'FALSE',...->False
    :param s:
    :return:
    '''
    if not isinstance(s, str):
        raise ValueCastError("input value type is %s, expect string." % s.__class__.__name__)

    s = s.strip().lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        raise ValueCastError("input value is not bool string, expect true or false.")

def num2str(n):
    '''
        number value to string, including int, long, float types
        123->'123'
        1.2->'1.2'
    :param n:
    :return:
    '''
    if not (isinstance(n, int) or isinstance(n, float) or isinstance(n, long)):
        raise ValueCastError("input value type is %s, expect int,long or float." % n.__class__.__name__)
    return str(n)

def str2num(s):
    '''
        string to relate type of number value
    :param s:
    :return:
    '''
    if not isinstance(s, str):
        raise ValueCastError("input value type is %s, expect string." % s.__class__.__name__)
    return typecls(s)(s)

def isnum(str):
    '''
        test if str is numeric
    :param str:
    :return:
    '''
    import re
    numreg = re.compile(r'\d')
    if numreg.match(str):
        return True
    return False

def numcls(s):
    '''
        detect number type class from input numeric string
    :param s:
    :return:
    '''
    if s.find('.') != -1:
        return float
    else:
        v = int(s)
        if isinstance(v, int):
            return int
        else:
            return long

def typecls(s):
    '''
        detect type class from input string
    :param s:
    :return:
    '''
    s = s.lower()

    if s=='none' or s=='null':
        # test none
        return None
    elif s=='true' or s=='false':
        # test boolean
        return bool
    elif isnum(s):
        # test numeric
        return numcls(s)
    else:
        #string
        return str

def objtostr(obj, escaped=None):
    '''
        object to string
    :param obj:
    :return:
    '''
    castfunc = {int.__name__:num2str, float.__name__:num2str, long.__name__:num2str, bool.__name__:bool2str, None.__class__.__name__:none2str}

    s = castfunc.get(obj.__class__.__name__, str)(obj)
    if escaped:
        for c in escaped:
            s = s.replace(c, "%"+str(hex(ord(c))))
    return s

def str2obj(s, escaped=None):
    '''
        string to object
    :param str:
    :return:
    '''
    castfunc = {int: str2num, float: str2num, long: str2num, bool: str2bool, None: str2none}

    if escaped:
        for c in escaped:
            s = s.replace("%"+str(hex(ord(c))), c)

    obj = castfunc.get(typecls(s), str)(s)

    return obj


if __name__ == "__main__":
    print objtostr("123", ",|")

    print str2obj("123.4")