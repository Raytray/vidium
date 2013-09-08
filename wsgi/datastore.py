import pymongo
import os
import pafy

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

        coll.ensure_index('_id', ASCENDING)

        the_collection = coll

    return the_collection


def get_user_data(token):
    """Returns user data if token is found"""
    coll = get_mongo_collection()
    user_data = coll.find_one({'_id': token})
    if not user_data:
        return None
    else:
        return user_data


def delete(token, url):
    """Delete given url, returns True if sucessful"""
    coll = get_mongo_collection()
    user_data = get_user_data(token)

    if not user_data:
        return "User not Found"

    new_vid_list = []
    delete = False

    for vid in user_data['vids']:
        if vid['url'] not in url:
            new_vid_list.append(vid)
        else:
            delete = True

    user_data['vids'] = new_vid_list
    coll.save(user_data)
    return delete


def retrieve(token, tags=None):
    """Get all stored videos with tags"""
    coll = get_mongo_collection()
    results_list = []

    user_data = get_user_data(token)
    if not user_data:
        return "User not found"

    if not tags:
        results_list = user_data['vids']

    else:
        for vid in user_data['vids']:
            if all(tag in vid['tags'] for tag in tags):
                results_list.append(vid)

    return results_list[::-1]


def store(token, url, tags):
    """Store url and tags."""
    coll = get_mongo_collection()

    old_item = get_user_data(token)

    video_obj = pafy.Pafy(url)
    if hasattr(video_obj, 'bigthumbhd'):
        thumb = video_obj.bigthumbhd
    else:
        thumb = video_obj.thumb

    tags.append(video_obj.title.split(" "))
    if old_item:
        for video in old_item['vids']:
          if video['url'] == url:
                video['tags'] = tags
                return coll.save(old_item)

        old_item['vids'].append({'url': url,
                                 'tags': tags,
                                 'title': video_obj.title,
                                 'thumb_url': thumb,
                                 'duration': video_obj.duration})
        return coll.save(old_item)

    else:
        new_item = {'_id': token,
                    'vids': [{'url': url,
                              'tags': tags,
                              'title': video_obj.title,
                              'thumb_url': thumb,
                              'duration': video_obj.duration,
                              }]
                    }
    return coll.insert(new_item)
