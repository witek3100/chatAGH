import json
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