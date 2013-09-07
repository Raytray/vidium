import pymongo
import os

from collections import defaultdict

host = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
port = os.environ.get('OPENSHIFT_MONGODB_DB_PORT')

mongo_pass = os.environ.get('MONGO_PASS')

the_collection = None

from pymongo import MongoClient, ASCENDING


def get_mongo_collection():
    """Inits and returns global the_connection if not
    initialized with default collection."""
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


def retrieve(tags=None):
    """Get all stored videos with tags"""
    coll = get_mongo_collection()

    results_dict = defaultdict(list)

    if not tags:
        for item in coll.find({},{'_id': 0}):
            results_dict[item['url']].extend(item['tags'])

    else:
        for item in coll.find({'tags': {'$all': tags}}, {'_id': 0}):
            results_dict[item['url']].extend(item['tags'])

    return [{'url': url, 'tags': list(set(tags))} for url, tags in dict(results_dict).iteritems()]



def store(url, tags):
    """Store url and tags."""
    coll = get_mongo_collection()

    new_item = {"url": url,
                 "tags": tags}

    return coll.insert(new_item)
