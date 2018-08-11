from .exception import *
import shutil
import syncer
import asyncio
import json
import os


class KeybaseCmdWrapper():
    def __init__(self, keybase_exec="keybase"):
        if keybase_exec == "keybase" and shutil.which("keybase") is not None:
            pass
        elif shutil.which(
                "keybase", path=os.path.dirname(
                    os.path.abspath(keybase_exec))) is not None:
            pass
        else:
            raise KeybaseException("keybase executable not found")
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
        return json.loads(await self.exec_keybase_cmd(
            "chat", "api", stdindata=json.dumps(data).encode("utf-8")))

    def exec_keybase_chat_api_sync(self, data):
        return syncer.sync(self.exec_keybase_chat_api(data))
