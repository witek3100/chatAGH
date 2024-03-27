
import datetime
import markdown

from langchain_core.messages import AIMessage, HumanMessage, AnyMessage

from src.utils import messages_collection, logger


class Message:
    def __init__(self, content, id=None, chat_id=None, agent='any', timestamp=datetime.datetime.now(), source=[]):
        self.id = id
        self.chat_id = chat_id
        self.timestamp = timestamp

        self.agent = agent
        self.message = self._get_agent_class()(content=content)
        self.source = source

        self.save()

    def _get_agent_class(self):
        agents = {
            'bot': AIMessage,
            'human': HumanMessage,
            'any': AnyMessage
        }
        return agents[self.agent]

    @property
    def content_html(self):
        return markdown.markdown(self.message.content)

    def save(self):
        logger.log(f'Adding new {self.agent} message to db: {self.message.content}')
        messages_collection.insert_one({
            'chat_id': self.chat_id,
            'content': self.message.content,
            'agent': self.agent,
            'timestamp': self.timestamp,
            'source': self.source
        })


