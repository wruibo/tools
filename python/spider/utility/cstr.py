'''
    string tools
'''


def strips(strs, chars=None):
    stripeds = []
    for str in strs:
        stripeds.append(str.strip(chars))
    return stripeds

class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        if self.a == other.a and self.b == other.b:
            return True
        return False


if __name__ == "__main__":
    d = A(1, 2)
    c = A(1, 2)

    if d == c:
        print "eq"