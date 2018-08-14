import keybasechat
import pytest
import pprint

class TestClass():

    @pytest.fixture(scope="class")
    def init_client(self):
        self.client = keybasechat.KeybaseCmdWrapper()

    def get_conversations(self):
        self.init_client()
        return self.client.list_conversation_sync()
    
    def test_read_msg_list(self):
        conversationlist = self.get_conversations()
        assert len(conversationlist.conversations)>1

    def test_read_conversation(self):
        conversationlist = self.get_conversations()
        conversation = conversationlist.conversations[0]
        assert conversation.id
