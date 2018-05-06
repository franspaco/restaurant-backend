import os
from flask import g, current_app
from pymongo import MongoClient


def get_db():
    if 'db' not in g:
        g.db = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT'])).restaurants
    return g.db

def save_kv(key, value):
    kvstore = get_db().kvstore
    kvstore.replace_one({'key':key}, {"key":key, "value": value}, upsert=True)

def load_kv(key):
    kvstore = get_db().kvstore
    res = kvstore.find_one({'key':key})

    if res is None:
        return None
    else:
        return res['value']
