import os
import json
import sys
import logging
import traceback
import pymongo
from datetime import datetime

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeStore

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

config_path = os.path.join(project_root, 'src', 'configs', 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

source_domains_path = os.path.join(project_root, 'src', 'sources', 'source_domains.json')
with open(source_domains_path) as domains:
    domains = json.load(domains)

os.environ['PINECONE_API_KEY'] = config['pinecone']['api_key']
os.environ['OPENAI_API_KEY'] = config['openai']['api_key']


# MONGO CLIENT
mongo_uri = config["mongo"]["uri"]
mongo_db = config["mongo"]["db"]
mongo_client = pymongo.MongoClient(mongo_uri)[mongo_db]

chats_collection = mongo_client["chats"]
messages_collection = mongo_client["messages"]
logs_collection = mongo_client["logs"]


# PINECONE INDEX
pinecone_env = config['pinecone']['environment']
index_name = config['pinecone']['index_name']

embeddings = OpenAIEmbeddings()

docsearch = PineconeStore.from_existing_index(index_name, embeddings)
retriever = docsearch.as_retriever()


# LOGGER
class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)

    def log(self, message):
        tb = traceback.extract_stack()

        filename, line_no, function_name, _ = tb[0]

        log_data = {
            'message': message,
            'timestamp': datetime.now(),
            'traceback': str(tb),
        }

        self.logger.info(f"{message} (Source: {log_data['traceback']})")
        logs_collection.insert_one(log_data)

logger = Logger()
