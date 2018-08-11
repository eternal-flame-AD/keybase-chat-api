from .internal import KeybaseApiDataset
from .message import KeybaseMessage
import datetime
import syncer


class KeybaseConversation(KeybaseApiDataset):
    def __init__(self):
        raise RuntimeError("KeybaseConversation cannot be constructed")


class KeybaseConversationFromList(KeybaseConversation):
    def __init__(self, conversationdata):
        self.id = conversationdata['id']
        self.unread = conversationdata['unread']
        self.active_at = datetime.datetime.fromtimestamp(
            conversationdata['active_at'])
        channel = conversationdata['channel']
        self.name = channel['name']
        self.public = channel['public']
        self.members_type = channel['members_type']
        self.topic_type = channel['topic_type']


class KeybaseConversationFromRead(KeybaseConversation):
    def __init__(self, conversationdata, apiclient=None):
        self.__apiclient = apiclient
        self.channel_name = conversationdata['channel']['name']
        self._next_page = conversationdata['pagination']['next']
        self._prev_page = conversationdata['pagination']['prev']
        self.num = conversationdata['pagination']['num']
        self.is_last = conversationdata['pagination']['last']
        self.messages = [
            KeybaseMessage(msg) for msg in conversationdata['messages']
        ]

    async def next_page(self):
        return await self.__apiclient.read_conversation(
            self.channel_name, self.num, self._next_page)

    def next_page_sync(self):
        return syncer.sync(self.next_page())

    async def prev_page(self):
        return await self.__apiclient.read_conversation(
            self.channel_name, self.num, self._prev_page)

    def prev_page_sync(self):
        return syncer.sync(self.prev_page())
