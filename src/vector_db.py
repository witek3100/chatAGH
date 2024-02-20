import pinecone
import json
import os

from langchain.embeddings.openai import OpenAIEmbeddings

from sources_loader import load_sources

with open("config.json") as config_file:
    config = json.load(config_file)

openai_api_key = config["openai"]["api_key"]
pinecone_api_key = config["pinecone"]["api_key"]
index_name = "agh-statutes"


def init_index():
    docs = load_sources()

    embeddings = OpenAIEmbeddings(api_key=openai_api_key)

    pc = pinecone.Pinecone(api_key=pinecone_api_key)
    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            metric="cosine",
            dimension=1536,
            spec=pinecone.PodSpec(environment=os.environ["PINECONE_API_ENV"])
        )
        pc_index = pc.from_documents(docs, embeddings, index_name=index_name)

    else:
        pc_index = pc.from_existing_index(index_name, embeddings)

    docsearch = pc.from_documents(docs, embeddings, index_name=index_name)


def similarity_search():
    pass


if __name__ == '__main__':
    init_index()