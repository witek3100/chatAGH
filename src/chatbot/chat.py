from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.sources.vector_db import retriever


class Chat:
    def __init__(self, chat_id=None):
        self.history = []
        self.id = chat_id
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

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_chain
        else:
            return input["question"]

    def ask(self, question):
        answer = self.chain.invoke({"question": question, "chat_history": self.history})
        self.history.append(HumanMessage(content=question))
        self.history.append(answer)
        self.save()

        return answer

    def save(self):
        pass


if __name__ == "__main__":
    chat = Chat()
    print(chat.ask("Zmiana kierunku studiów"))