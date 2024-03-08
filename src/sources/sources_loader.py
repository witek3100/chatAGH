import os
import json

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.utils import config, sources

def load_sources():
    documents = []

    # Load AGH statutes pdf documents
    print('Loading AGH statutes')
    for statute_link in sources['statutes']:
        try:
            statute_docs = load_pdf(statute_link)
            documents.extend(statute_docs)
        except Exception as e:
            print(f"Error while loading doc: {statute_link}, error message: {e}")
            pass

    return documents

def load_pdf(link):
    loader = PyPDFLoader(link)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["sources_loader"]["chunk_size"],
        chunk_overlap=config["sources_loader"]["chunk_overlap"]
    )
    docs = text_splitter.split_documents(data)

    return docs


def load_html():
    pass