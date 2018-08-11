from .internal import KeybaseApiDataset
from .conversation import KeybaseConversationFromList


class KeybaseConversationList(KeybaseApiDataset):
    def __init__(self, apiresp, offline_ok=False):
        if not offline_ok:
            super().checkoffline(self, apiresp)
        self.conversations = [
            KeybaseConversationFromList(c) for c in apiresp['conversations']
        ]
