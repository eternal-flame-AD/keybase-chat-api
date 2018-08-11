from .exception import KeybaseOfflineException


class KeybaseApiDataset():
    def __init__(self, apidata):
        pass

    @staticmethod
    def checkoffline(cls, apidata):
        if 'offline' in apidata and apidata['offline']:
            raise KeybaseOfflineException()
