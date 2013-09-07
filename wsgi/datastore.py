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
    global the_collection
    if not the_collection:
        if host:
            mongo = MongoClient(host, int(port))
        else:
            mongo = MongoClient()

        db = mongo['vidium']
        coll = db['user_data']
        db.authenticate("admin", mongo_pass)

        coll.ensure_index([('_id', ASCENDING),
                           ('vids.tags', ASCENDING)])

        the_collection = coll

    return the_collection


def retrieve(token, tags=None):
    """Get all stored videos with tags"""
    coll = get_mongo_collection()

    results_list = []

    user_data = coll.find_one({'_id': token},
                              {'_id': 0})

    if not user_data:
        return []

    elif not tags:
        for vid in user_data['vids']:
            results_list = user_data['vids']

    else:
        for vid in user_data['vids']:
            if all(tag in vid['tags'] for tag in tags):
                results_list.append(vid)

    return results_list


def store(token, url, tags):
    """Store url and tags."""
    coll = get_mongo_collection()

    old_item = coll.find_one({'_id': token})
    if old_item:
        for video in old_item['vids']:
            if video['url'] == url:
                video['tags'] = tags
                return coll.save(old_item)
        old_item['vids'].append({'url': url, 'tags': tags})
        return coll.save(old_item)

    else:
        new_item = {'_id': token,
                    'vids': [{'url': url,
                              'tags': tags}]
                    }
        return coll.insert(new_item)
