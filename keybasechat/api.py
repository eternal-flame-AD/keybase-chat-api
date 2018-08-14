from .exception import *
from .conversation import KeybaseConversationFromRead
from .conversationlist import KeybaseConversationList
from .message import KeybaseMessage
import shutil
import syncer
import asyncio
import json
import os
import uuid
import tempfile


class KeybaseCmdWrapper():
    def __init__(self, keybase_exec="keybase", offline_ok=False):
        if keybase_exec == "keybase" and shutil.which("keybase") is not None:
            pass
        elif shutil.which(
                "keybase", path=os.path.dirname(
                    os.path.abspath(keybase_exec))) is not None:
            pass
        else:
            raise KeybaseException("keybase executable not found")
        self.offline_ok = offline_ok
        self.exec_path = keybase_exec
        self.temp_dir=None

    async def exec_keybase_cmd(self, *args, stdindata=None):
        proc = await asyncio.create_subprocess_exec(
            self.exec_path,
            *args,
            stdin=asyncio.subprocess.PIPE if stdindata else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate(stdindata)
        if len(stderr) > 0:
            raise KeybaseCliException("\n" + stderr.decode())
        return stdout.decode()

    def exec_keybase_cmd_sync(self, *args):
        return syncer.sync(self.exec_keybase_cmd(*args))

    async def exec_keybase_chat_api(self, data):
        res = json.loads(await self.exec_keybase_cmd(
            "chat", "api", stdindata=json.dumps(data).encode("utf-8")))
        if 'error' in res:
            raise KeybaseApiException(res['error'])
        return res['result']

    def exec_keybase_chat_api_sync(self, data):
        return syncer.sync(self.exec_keybase_chat_api(data))
    
    def init_temp_dir(self, dir=None):
        self.temp_dir = tempfile.TemporaryDirectory("keybasechat_", dir=dir)

    async def read_conversation(self,
                                channel,
                                pagination_num=None,
                                pagination_next=None,
                                peek=False,
                                unread_only=False):
        query = {
            "method": "read",
            "params": {
                "options": {
                    "channel": {
                        "name": str(channel)
                    },
                    "peek": peek,
                    "unread_only": unread_only,
                }
            }
        }
        if pagination_num:
            pageparam = {}
            pageparam['num'] = pagination_num
            if pagination_next:
                pageparam['next'] = pagination_next
            query['params']['options']['pagination'] = pageparam
        conversationdata = await self.exec_keybase_chat_api(query)
        return KeybaseConversationFromRead(conversationdata, channel, apiclient=self)

    def read_conversation_sync(self,
                               channel,
                               pagination_num=None,
                               pagination_next=None,
                               peek=False,
                               unread_only=False):
        return syncer.sync(
            self.read_conversation(
                channel,
                pagination_num,
                pagination_next,
                peek,
                unread_only,
            ))

    async def list_conversation(self, topic_type=None):
        if topic_type:
            query = {
                "method": "list",
                "params": {
                    "options": {
                        "topic_type": topic_type
                    }
                }
            }
        else:
            query = {"method": "list"}
        res = await self.exec_keybase_chat_api(query)
        return KeybaseConversationList(res, self.offline_ok)

    def list_conversation_sync(self, topic_type=None):
        return syncer.sync(self.list_conversation(topic_type))

    async def delete_message(self, channel, msg_id):
        query = {"method": "delete", "params": {"options": {"channel": {"name": channel}, "message_id": msg_id}}}
        await self.exec_keybase_chat_api(query)

    def delete_message_sync(self, channel, msg_id):
        return syncer.sync(self.delete_message(channel, msg_id))
    
    async def send_text(self, channel, text, public=False, team=False, topic_name=None):
        query = {"method": "send", "params": {"options": {"channel": {"name": channel}, "message": {"body": text}}}}
        if team:
            query['params']['options']['channel']['members_type']="team"
        if topic_name:
            query['params']['options']['channel']['topic_name']=topic_name
        if public:
            query['params']['options']['channel']['public'] = True
        await self.exec_keybase_chat_api(query)
    
    def send_text_sync(self, channel, text, public=False, team=False, topic_name=None):
        return syncer.sync(self.send_text(channel, text, public, team, topic_name))
    
    async def edit_text(self, channel, msg_id, text):
        query = {"method": "edit", "params": {"options": {"channel": {"name": channel}, "message_id": msg_id, "message": {"body": text}}}}
        await self.exec_keybase_chat_api(query)
    
    def edit_text_sync(self, channel, msg_id, text):
        return syncer.sync(self.edit_text(channel, msg_id, text))
    
    async def react_msg(self, channel, msg_id, text):
        query = {"method": "reaction", "params": {"options": {"channel": {"name": channel}, "message_id": msg_id, "message": {"body": text}}}}
        await self.exec_keybase_chat_api(query)
    
    def react_msg_sync(self, channel, msg_id, text):
        return syncer.sync(self.react_msg(channel, msg_id, text))
    
    async def upload_file(self, channel, filename, title=None):
        if title is None:
            title = os.path.basename(filename)
        query = {"method": "attach", "params": {"options": {"channel": {"name": channel}, "filename": filename, "title": title}}}
        await self.exec_keybase_chat_api(query)
    
    def upload_file_sync(self, channel, filename, title=None):
        return syncer.sync(self.upload_file(channel, filename, title))
    
    async def download_file_to_path(self, channel, msg_id, output_path):
        query = {"method": "download", "params": {"options": {"channel": {"name": channel}, "message_id": msg_id, "output": output_path}}}
        await self.exec_keybase_chat_api(query)
    
    def download_file_to_path_sync(self, channel, msg_id, output_path):
        return syncer.sync(self.download_file_to_path(channel, msg_id, output_path))
    
    async def read_file(self, channel, msg_id):
        if self.temp_dir is None:
            self.init_temp_dir()
        path = os.path.join(self.temp_dir, uuid.uuid1())
        await self.download_file_to_path(channel, msg_id, path)
        with open(path, mode="r") as f:
            return f.read()
        
    def read_file_sync(self, channel, msg_id):
        return syncer.sync(self.read_file(channel, msg_id))
    
    async def mute_conversation(self, channel):
        query = {"method": "setstatus", "params": {"options": {"channel": {"name": channel}, "status": "muted"}}}
        await self.exec_keybase_chat_api(query)
    
    def mute_conversation_sync(self ,channel):
        return syncer.sync(self.mute_conversation(channel))
    
    async def search_conversation_with_regex(self, channel, regex):
        query =  {"method": "searchregexp", "params": {"options": {"channel": {"name": channel}, "query": regex, "is_regex": True}}}
        return await self.exec_keybase_chat_api(query)
    
    def search_conversation_with_regex_sync(self, channel, regex):
        return syncer.sync(self.search_conversation_with_regex(channel, regex))
    
    async def mark_message_as_read(self, channel, msg_id):
        query = {"method": "mark", "params": {"options": {"channel": {"name": channel}, "message_id": msg_id}}}
        return await self.exec_keybase_chat_api(query)
    
    def mark_message_as_read_sync(self, channel, msg_id):
        return syncer.sync(self.mark_message_as_read(channel, msg_id))
    
