"""
    base type definition
"""


class Int(int):
    def __new__(cls, x, base=10):
        if isinstance(x, str) and x.strip()=="":
            return int(0)
        return int(x, base)


class Float(float):
    def __new__(cls, x):
        if isinstance(x, str) and x.strip()=="":
            return float(0.0)
        return float(x)


class String(str):
    def __new__(cls, x):
        return str(x)
