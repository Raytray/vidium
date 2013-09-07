import tldextract

import datastore

from collections import defaultdict
from flask import Flask, request, jsonify

app = Flask(__name__)

supported_services = ['vimeo', 'youtube']


@app.route('/api/retrieve/')
def api_retrieve():
    token = request.args.get('token')
    if token is None:
        return "Need valid google oauth token"

    tags = request.args.getlist('tags')
    return jsonify({'vids': datastore.retrieve(token, tags=tags)})


@app.route('/api/store/')
def api_store():
    token = request.args.get('token')
    if token is None:
        return "Need valid google oauth token"

    url = request.args.get('url')
    tags = request.args.getlist('tags')
    if url is None:
        return "need url parameter"
    elif tldextract.extract(url).domain not in supported_services:
        return "serivce has to be from one of these {}".format(
            supported_services)

    tags.sort()
    result = datastore.store(token, url, tags)
    if result:
        return "Thanks!"
    else:
        return "Something went wrong."


@app.route("/")
def index():
    return "Nothing to see here"


if __name__ == "__main__":
    app.debug = True
    app.run()
