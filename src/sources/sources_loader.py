
import os
import asyncio
import time
import threading

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone as PineconeStore

from src.utils import config, domains
from src.sources.domain_scrapper import DomainScrapper

os.environ['PINECONE_API_KEY'] = config['pinecone']['api_key']
os.environ['OPENAI_API_KEY'] = config['openai']['api_key']

pinecone_env = config['pinecone']['environment']
index_name = config['pinecone']['index_name']

embeddings = OpenAIEmbeddings()
pc = PineconeStore.from_existing_index(index_name, embeddings)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config["sources_loader"]["chunk_size"],
    chunk_overlap=config["sources_loader"]["chunk_overlap"]
)

def load_sources_to_index():

    # With threading
    threads = []
    for source_domain in domains['domains']:
        thread = threading.Thread(target=load_domain_async, args=(source_domain,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        time.sleep(2)
        thread.join()

    # Without threading
    # for source_domain in domains['domains']:
    #     await load_domain(source_domain)

    print("All sources added to Pinecone index")

def load_domain_async(domain):
    asyncio.run(load_domain(domain))

async def load_domain(domain):
    print(f'\n\n Loading knowledge sources from domain {domain} ...')
    urls = await DomainScrapper(domain).scrap_async()
    if len(urls) == 0:
        print(f'ERROR OCCURED WHILE LOADING {domain} TO PINECONE INDEX, NOTHING ADDED')
        return

    print(f'generating documents from scraped urls')
    documents = []
    for url in urls:
        if url.endswith('.pdf'):
            docs = load_pdf(url)
        else:
            docs = load_html(url)
        documents.extend(docs)

    print(f'all scraped urls loaded, {len(documents)} new documents created, generating embeddings and adding to index ...')
    pc.add_documents(documents)
    print(f'SOURCE {domain} ADDED TO PINECONE INDEX')


def load_pdf(link):
    loader = PyPDFLoader(link)
    data = loader.load()
    docs = text_splitter.split_documents(data)

    return docs

def load_html(link):
    try:
        loader = WebBaseLoader(link)
        data = loader.load()
        docs = text_splitter.split_documents(data)
        docs = [format_html(doc) for doc in docs]
        docs = [doc for doc in docs if len(doc.page_content) > 40]
    except Exception as e:
        print(f'Error loading documents from url {link}: {e}')
        return []
    return docs

def format_html(doc):
    doc.page_content = doc.page_content.replace('\n\n\n\n', '\n\n')
    return doc


if __name__ == '__main__':
    load_sources_to_index()