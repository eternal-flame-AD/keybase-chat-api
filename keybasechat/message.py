from .internal import KeybaseApiDataset
import datetime
import syncer

class KeybaseMessage(KeybaseApiDataset):
    def __init__(self, msgdata, apiclient=None, channel=None):
        self.__apiclient=apiclient
        self.channel=channel
        msg = msgdata['msg']
        self.id = msg['id']
        self.content_type = msg['content']['type']
        if self.content_type == "text":
            self.content = msg['content']['text']['body']
        elif self.content_type=="attachment":
            self.content = msg['content']
        elif self.content_type=="none":
            self.content = None
        else:
            print(msgdata)
            raise NotImplementedError(self.content_type)
        self.sender = msg[
            'sender']  #['device_id', 'device_name', 'uid', 'username']
        self.sent_at = datetime.datetime.fromtimestamp(msg['sent_at'])
        self.unread = msg['unread']

    async def mark_as_read(self):
        if self.unread:
            return await self.__apiclient.mark_message_as_read(self.channel.channel_name, self.id)
        return 
    
    def mark_as_read_sync(self):
        return syncer.sync(self.mark_as_read())

    async def delete(self):
        return await self.__apiclient.delete_message(self.channel.channel_name, self.id)
    
    def delete_sync(self):
        return syncer.sync(self.delete())
    
    async def edit_text(self, text):
        if self.content_type=='text':
            await self.__apiclient.edit_text(self.channel.channel_name, self.id, text)
            self.content = text
        else:
            raise NotImplementedError()
    
    def edit_text_sync(self, text):
        return syncer.sync(self.edit_text(text))
    