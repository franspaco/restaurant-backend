import os
from flask import g, current_app
from pymongo import MongoClient


def get_db():
    if 'db' not in g:
        g.db = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT'])).restaurants
    return g.db