import os
import datetime
import markdown

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.utils import chats_collection, messages_collection, retriever
from src.chatbot.message import Message

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Chat:
    def __init__(self, chat_id=None):
        self.history = []
        self.sources = []
        self.created = datetime.datetime.now()

        if chat_id:
            self.id = chat_id
            self.load_history()

        self.llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.2)

        prompt_path = os.path.join(project_root, 'chatbot/prompts/contextualize_prompt.txt')
        with open(prompt_path) as file:
            prompt_text = file.read()
            contextualize_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", prompt_text),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}")
                ]
            )
            self.contextualize_chain = contextualize_prompt | self.llm | StrOutputParser()

        prompt_path = os.path.join(project_root, 'chatbot/prompts/qa_prompt.txt')
        with open(prompt_path) as file:
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
        formated_docs = [f'## text: \n {doc.page_content} \n\n ## source: {doc.metadata["source"]}' for doc in docs]
        return "\n\n\n ### Context: \n".join(formated_docs)

    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_chain
        else:
            return input["question"]

    # def ask(self, question):
    #     msg_question = Message(
    #         chat_id=self.id,
    #         content=question,
    #         agent='human',
    #     )
    #
    #     history = [msg.message.content for msg in self.history]
    #     answer = self.chain.invoke({"question": question, "chat_history": history})
    #
    #     content, urls = self._parse_answer(answer)
    #
    #     msg_answer = Message(
    #         chat_id=self.id,
    #         content=content,
    #         agent='bot',
    #         source=urls
    #     )
    #
    #     self.history.extend([msg_question, msg_answer])
    #
    #     return msg_answer

    @staticmethod
    def get_streaming_response(question, chat_id):
        try:
            chat = Chat(chat_id=chat_id)
            msg_question = Message(
                chat_id=chat.id,
                content=question,
                agent='human',
            )

            content = ''
            history = [msg.message.content for msg in chat.history]
            for token in chat.chain.stream({"question": question, 'chat_history': history}):
                content += token.content
                content_html = markdown.markdown(content).replace('\n', '')
                yield f"data: {content_html}\n\n"

            msg_answer = Message(
                chat_id=chat.id,
                content=content,
                agent='bot',
            )
            chat.history.extend([msg_question, msg_answer])

            yield 'data: <!END>\n\n'

        except Exception as e:
            print(f'Error while generating response: {e}')
            yield 'data: <!ERROR>\n\n'

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
                    timestamp=message['timestamp'],
                    source=message['source']
                )
            self.history.append(msg)

    def _parse_answer(self, answer):
        split = answer.content.split('## links:')
        answer = split[0]
        try:
            urls = [url for url in split[1].split('\n') if len(url) > 5]
        except IndexError:
            urls = []
        return answer, urls


if __name__ == "__main__":
    chat = Chat()
    print(chat.ask("Zmiana kierunku studiów"))