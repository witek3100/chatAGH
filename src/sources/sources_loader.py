import os
import json
import urllib.request

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.utils import config, sources

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config["sources_loader"]["chunk_size"],
    chunk_overlap=config["sources_loader"]["chunk_overlap"]
)

def load_sources():
    documents = []

    # Load pdf documents
    print('Loading pdfs')
    for pdf in sources["pdf"]:
        try:
            url = pdf["url"]
            statute_docs = load_pdf(url)
            documents.extend(statute_docs)
        except Exception as e:
            print(f"Error while loading doc: {url}, error message: {e}")
            pass

    # Load html websites
    print('Loading htmls')
    for i, source_url in enumerate(sources["html"]):
        if i % 50 == 0:
            print(f'{i} out of {len(sources["html"])} documents loaded')
        try:
            doc = load_html(source_url)
            documents.extend(doc)
        except Exception as e:
            print(f"Error while fetching file {source_url}, error message: {e}")
            continue

    print(f'Total of {len(documents)} loaded')

    return documents

def load_pdf(link):
    loader = PyPDFLoader(link)
    data = loader.load()
    docs = text_splitter.split_documents(data)

    return docs

def load_html(link):
    loader = WebBaseLoader(link)
    data = loader.load()
    docs = text_splitter.split_documents(data)

    return docs

