'''
    value verifier
'''


class Verifier:
    def __init__(self):
        pass

    def verify(self, value):
        pass


class DefaultVerifier(Verifier):
    def __init__(self):
        pass

    def verify(self, value):
        return True


class RegexVerifier(Verifier):
    def __init__(self, regex):
        pass

    def verify(self, value):
        pass
