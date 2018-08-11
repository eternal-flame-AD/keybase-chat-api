class KeybaseException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class KeybaseCliException(KeybaseException):
    def __init__(self, msg):
        super().__init__("Keybase cli said on stderr: " + msg)


class KeybaseApiException(KeybaseException):
    def __init__(self, msg):
        super().__init__(msg)


class KeybaseOfflineException(KeybaseException):
    def __init__(self):
        super().__init__(
            "Keybase returned offline status. Check your network connection.")
