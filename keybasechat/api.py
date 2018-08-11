from .exception import *
from .conversation import KeybaseConversationFromRead
from .conversationlist import KeybaseConversationList
from .message import KeybaseMessage
import shutil
import syncer
import asyncio
import json
import os


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
        return KeybaseConversationFromRead(conversationdata, apiclient=self)

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

    def list_coversation_sync(self, topic_type=None):
        return syncer.sync(self.list_conversation(topic_type))
