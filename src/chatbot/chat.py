import datetime
import langchain_core.messages

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.sources.vector_db import retriever
from src.utils import chats_collection, messages_collection


class Chat:
    def __init__(self, chat_id=None):
        self.history = []
        if chat_id:
            self.id = chat_id
            self.load()
        else:
            self.id = 0
            self.load()

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        with open('src/chatbot/prompts/contextualize_prompt.txt', 'r') as file:
            prompt_text = file.read()
            contextualize_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", prompt_text),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}")
                ]
            )
            self.contextualize_chain = contextualize_prompt | self.llm | StrOutputParser()

        with open('src/chatbot/prompts/qa_prompt.txt', 'r') as file:
            prompt_text = file.read()
            self.qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", prompt_text),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}")
                ]
            )

        self.chain = (
            RunnablePassthrough.assign(
                context=self.contextualized_question | retriever | self.format_docs
            )
            | self.qa_prompt
            | self.llm
        )

        self.save()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_chain
        else:
            return input["question"]

    def ask(self, question):

        messages_collection.insert_one({
            'content': question,
            'chat_id': self.id,
            'timestamp': datetime.datetime.now(),
            'agent': 'human'
        })

        answer = self.chain.invoke({"question": question, "chat_history": self.history})
        messages_collection.insert_one({
            'content': answer.content,
            'chat_id': self.id,
            'timestamp': datetime.datetime.now(),
            'agent': 'bot'
        })

        return answer

    def save(self):
        chat = {
            'id': self.id,
            'llm': self.llm.model_name,
        }
        update = {"$setOnInsert": chat}
        chats_collection.update_one({"id": self.id}, update, True)

    def load(self):
        query = {"chat_id": self.id}
        sort = {"timestamp": 1}
        for message in messages_collection.find(query).sort(sort):
            print(message)
            if message["agent"] == "human":
                agent_class = HumanMessage
            elif message["agent"] == "bot":
                agent_class = AIMessage
            else:
                agent_class = AnyMessage
            self.history.append(agent_class(content=message["content"]))


if __name__ == "__main__":
    chat = Chat()
    print(chat.ask("Zmiana kierunku studiów"))