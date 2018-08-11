
class KeybaseException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class KeybaseCliException(KeybaseException):
    def __init__(self, msg):
        super().__init__("Keybase cli said on stderr: "+msg)
