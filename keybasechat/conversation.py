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
    def __init__(self, conversationdata, channel_name, apiclient=None):
        self.__apiclient = apiclient
        self.channel_name = channel_name
        self._next_page = conversationdata['pagination']['next']
        self._prev_page = conversationdata['pagination']['previous']
        self.num = conversationdata['pagination']['num']
        self.is_last = conversationdata['pagination']['last']
        self.messages = [
            KeybaseMessage(msg, self.__apiclient, self) for msg in conversationdata['messages']
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

    async def mute(self):
        return await self.__apiclient.mute_conversation(self.channel_name)
    
    def mute_sync(self):
        return syncer.sync(self.mute())
    
    async def search_with_regex(self, regex):
        return await self.__apiclient.search_conversation_with_regex(self.channel_name, regex)
    
    def search_with_regex_sync(self, regex):
        return syncer.sync(self.search_with_regex(regex))
    
    async def send_text(self, text, public=False, team=False):
        return await self.__apiclient.send_text(self.channel_name, text, public, team)
    
    def send_text_sync(self, text, public=False , team=False):
        return syncer.sync(self.send_text(text, public, team))
    