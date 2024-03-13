
import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.sources.vector_db import retriever
from src.utils import chats_collection, messages_collection
from src.chatbot.message import Message


class Chat:
    def __init__(self, chat_id=None):
        self.history = []
        self.created = datetime.datetime.now()

        if chat_id:
            self.id = chat_id
            self.load_history()

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

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

        with open('src/chatbot/prompts/qa_prompt_pl.txt', 'r') as file:
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

        if not chat_id:
            self.save()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_chain
        else:
            return input["question"]

    def ask(self, question):
        msg_question = Message(
            chat_id=self.id,
            content=question,
            agent='human',
        )

        history = [msg.message.content for msg in self.history]
        answer = self.chain.invoke({"question": question, "chat_history": history})
        msg_answer = Message(
            chat_id=self.id,
            content=answer.content,
            agent='bot'
        )

        self.history.extend([msg_question, msg_answer])

        return answer

    def save(self):
        chat = {
            'llm': self.llm.model_name,
            'timestamp': self.created
        }
        result = chats_collection.insert_one(chat)
        self.id = result.inserted_id

    def load_history(self):
        query = {"chat_id": self.id}
        sort = {"timestamp": 1}

        for message in messages_collection.find(query).sort(sort):
            msg = Message(
                    id=message['_id'],
                    content=message['content'],
                    agent=message['agent'],
                    timestamp=message['timestamp']
                )
            self.history.append(msg)


if __name__ == "__main__":
    chat = Chat()
    print(chat.ask("Zmiana kierunku studiów"))