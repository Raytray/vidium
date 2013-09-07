import pymongo
import os

host = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
port = os.environ.get('OPENSHIFT_MONGODB_DB_PORT')

mongo_pass = os.environ.get('MONGO_PASS')

from pymongo import MongoClient

def mongo_test():
    if host:
        mongo = MongoClient(host, int(port))
    else:
        mongo = MongoClient()

    db = mongo['vidium']
    coll = db['test']

    db.authenticate("admin", mongo_pass)

    test_post = {"auth": "ray",
                 "num": 1}

    coll.insert(test_post)

    return coll.find_one()
