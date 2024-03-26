import os
import json
import logging
import traceback
import pymongo
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

config_path = os.path.join(project_root, 'src', 'configs', 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

sources_path = os.path.join(project_root, 'src', 'sources', 'sources.json')
with open(sources_path) as sources_file:
    sources = json.load(sources_file)

source_domains_path = os.path.join(project_root, 'src', 'sources', 'source_domains.json')
with open(source_domains_path) as domains:
    domains = json.load(domains)

mongo_uri = config["mongo"]["uri"]
mongo_db = config["mongo"]["db"]
mongo_client = pymongo.MongoClient(mongo_uri)[mongo_db]

chats_collection = mongo_client["chats"]
messages_collection = mongo_client["messages"]
logs_collection = mongo_client["logs"]

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def log(self, message):
        _, _, tb = traceback.stack_trace()

        filename, line_no, function_name, _ = tb[0]

        log_data = {
            'message': message,
            'timestamp': datetime.now(),
            'source': f"{filename}:{line_no} - {function_name}",
        }

        self.logger.info(f"{message} (Source: {log_data['source']})")
        logs_collection.insert_one(log_data)

logger = Logger()
