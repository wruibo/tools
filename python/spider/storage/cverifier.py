'''
    value verifier
'''


class Verifier:
    def __init__(self):
        pass

    class Base:
        def __init__(self):
            pass

        def verify(self, value):
            pass

    class DefaultVerifier(Base):
        def __init__(self):
            pass

        def verify(self, value):
            return True

    class RegexVerifier(Base):
        def __init__(self, regex):
            pass

        def verify(self, value):
            pass
