import pinecone
import json
import os

import bs4
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain_core.runnables import RunnableParallel

from src.sources.sources_loader import load_sources

with open("../config.json") as config_file:
    config = json.load(config_file)

os.environ['PINECONE_API_KEY'] = config['pinecone']['api_key']
os.environ['OPENAI_API_KEY'] = config['openai']['api_key']

pinecone_env = config['pinecone']['environment']
index_name = config['pinecone']['index_name']

pc = pinecone.Pinecone(environment=pinecone_env)
embeddings = OpenAIEmbeddings()

docsearch = PineconeStore.from_existing_index(index_name, embeddings)
retriever = docsearch.as_retriever()

def init_index():

    docs = load_sources()

    if index_name in (index['name'] for index in pc.list_indexes()):
        delete_response = pc.delete_index(index_name)
        if delete_response:
            print(f'Error while deleting index: {delete_response}')
        else:
            print(f'Pinecone index {index_name} deleted')

    pc.create_index(
        name=index_name,
        metric="cosine",
        dimension=1536,
        spec=pinecone.PodSpec(environment=pinecone_env)
    )
    PineconeStore.from_documents(docs, embeddings, index_name=index_name)

def search_docs(query, num_docs=4):
    print(f'Searching for {num_docs} docs for query: {query}')
    docs = docsearch.similarity_search(query, k=num_docs)

    for doc in docs:
        print(f"Doc found: \n {doc.page_content} \n\n")

    return docs


if __name__ == '__main__':
    init_index()