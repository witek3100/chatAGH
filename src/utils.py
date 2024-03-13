import json
import logging
import traceback
from datetime import datetime

import pymongo

with open("src/configs/config.json") as config_file:
    config = json.load(config_file)

with open("src/sources/sources.json") as sources_file:
    sources = json.load(sources_file)

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