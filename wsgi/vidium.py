import datastore

from collections import defaultdict
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/store/')
def api_store():
    url = request.args.get('url')
    tags = request.args.getlist('tags')
    if url is None:
        return "need url parameter"

    tags.sort()
    result = datastore.store(url, tags)
    if result:
        return "yay"
        #return "Successful url insert of {} with tags {}".format(url, tags)
    else:
        return "Something went wrong."


@app.route("/")
def hello():
    return "Nothing to see here"

if __name__ == "__main__":
    app.debug = True
    app.run()
