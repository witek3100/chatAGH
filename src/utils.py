import json

with open("config.json") as config_file:
    config = json.load(config_file)

with open("sources.json") as sources_file:
    sources = json.load(sources_file)