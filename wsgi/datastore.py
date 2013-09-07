import pymongo
import os

host = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
port = os.environ.get('OPENSHIFT_MONGODB_DB_PORT')

mongo_pass = os.environ.get('MONGO_PASS')

from pymongo import MongoClient, ASCENDING

def get_mongo_collection():
    if host:
        mongo = MongoClient(host, int(port))
    else:
        mongo = MongoClient()

    db = mongo['vidium']
    coll = db['user_data']
    db.authenticate("admin", mongo_pass)

    coll.ensure_index([('url', ASCENDING),
                       ('tags', ASCENDING)])

    return coll

def store(url, tags):
    coll = get_mongo_collection()

    new_item = {"url": url,
                 "tags": tags}

    return coll.insert(new_item)
