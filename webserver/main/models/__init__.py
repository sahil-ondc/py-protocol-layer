import json
from flask import request, g
from pymongo import MongoClient

from main.config import get_config_by_name
from main.logger.custom_logging import log

mongo_client = None
mongo_db = None


class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def initialize_before_calls(app):
    @app.before_request
    def set_page(page=1):
        page = int(request.args.get('page', 1))
        g.page = page


def init_database():
    global mongo_client, mongo_db
    if mongo_client and mongo_db:
        return
    database_host = get_config_by_name('MONGO_DATABASE_HOST')
    database_port = get_config_by_name('MONGO_DATABASE_PORT')
    database_name = get_config_by_name('MONGO_DATABASE_NAME')
    mongo_client = MongoClient(database_host, database_port)
    mongo_db = mongo_client[database_name]
    log(f"Connection to mongodb://{database_host}:{database_port} is successful!")
    create_all_ttl_indexes()
    log(f"Created indexes if not already present!")


def create_all_ttl_indexes():
    collection_names = ["on_search_items", "on_select", "on_init", "on_confirm", "on_cancel", "on_status", "on_support",
                        "on_track", "on_update", "on_rating"]
    [create_ttl_index(c) for c in collection_names]


def create_ttl_index(collection_name):
    ttl_in_seconds = get_config_by_name('TTL_IN_SECONDS')
    mongo_db[collection_name].create_index("created_at", name="created_at_ttl", expireAfterSeconds=ttl_in_seconds)


def get_mongo_collection(collection_name):
    if not mongo_client or not mongo_db:
        init_database()
    return mongo_db[collection_name]
