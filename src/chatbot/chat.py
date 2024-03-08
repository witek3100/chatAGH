import bs4
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel

from src.sources.vector_db import retriever


class Chat:
    def __init__(self, chat_id=None):
        self.history = []
        self.id = chat_id
        if chat_id:
            pass

    @staticmethod
    def answer_with_context(query, skill=None):
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
                RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
                | prompt
                | llm
                | StrOutputParser()
        )

        rag_chain = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain)

        return rag_chain.invoke(query)

    def ask(self, query):
        self.history.append(query)
        msg = Chat.answer_with_context(query)['answer']
        self.history.append(msg)
        self.save()

    def save(self):
        pass


if __name__ == "__main__":
    print(Chat.answer_with_context("Zmiana kierunku studiów"))