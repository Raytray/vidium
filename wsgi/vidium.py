import datastore

from collections import defaultdict
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/retrieve/')
def api_retrieve():
    tags = request.args.getlist('tags')
    return jsonify({'vids': datastore.retrieve(tags=tags)})


@app.route('/api/store/')
def api_store():
    url = request.args.get('url')
    tags = request.args.getlist('tags')
    if url is None:
        return "need url parameter"

    tags.sort()
    result = datastore.store(url, tags)
    if result:
        return "Thanks!"
    else:
        return "Something went wrong."


@app.route("/")
def hello():
    return "Nothing to see here"

if __name__ == "__main__":
    app.debug = True
    app.run()
