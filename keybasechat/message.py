from .internal import KeybaseApiDataset
import datetime


class KeybaseMessage(KeybaseApiDataset):
    def __init__(self, msgdata):
        msg = msgdata['msg']
        self.id = msg['id']
        self.content_type = msg['content']['type']
        if self.content_type == "text":
            self.content = msg['content']['text']['body']
        else:
            raise NotImplementedError(self.content_type)
        self.sender = msg[
            'sender']  #['device_id', 'device_name', 'uid', 'username']
        self.sent_at = datetime.datetime.fromtimestamp(msg['send_at'])
        self.unread = msg['unread']
