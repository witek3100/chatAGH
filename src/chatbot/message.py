
import datetime

from langchain_core.messages import AIMessage, HumanMessage, AnyMessage

from src.utils import messages_collection


class Message:
    def __init__(self, content, id=None, chat_id=None, agent='any', timestamp=datetime.datetime.now()):
        self.id = id
        self.chat_id = chat_id
        self.timestamp = timestamp

        self.agent = agent
        self.message = self._get_agent_class()(content=content)

        self.save()

    def _get_agent_class(self):
        agents = {
            'bot': AIMessage,
            'human': HumanMessage,
            'any': AnyMessage
        }
        return agents[self.agent]

    def save(self):
        messages_collection.insert_one({
            'chat_id': self.chat_id,
            'content': self.message.content,
            'agent': self.agent,
            'timestamp': self.timestamp
        })


