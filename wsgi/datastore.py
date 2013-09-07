import pymongo
import os

host = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
port = os.environ.get('OPENSHIFT_MONGODB_DB_PORT')

mongo_pass = os.environ.get('MONGO_PASS')

the_collection = None

from pymongo import MongoClient, ASCENDING


def get_mongo_collection():
    if not the_collection:
        global the_collection

        if host:
            mongo = MongoClient(host, int(port))
        else:
            mongo = MongoClient()

        db = mongo['vidium']
        coll = db['user_data']
        db.authenticate("admin", mongo_pass)

        coll.ensure_index([('url', ASCENDING),
                           ('tags', ASCENDING)])
        the_collection = coll

    return the_collection


def retrieve():
    coll = get_mongo_collection()

    return_list = []

    for item in coll.find({},{'_id': 0}):
        return_list.append(item)

    return return_list


def store(url, tags):
    coll = get_mongo_collection()

    new_item = {"url": url,
                 "tags": tags}

    return coll.insert(new_item)
