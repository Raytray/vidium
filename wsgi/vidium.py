import tldextract

import datastore

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

supported_services = ['youtube']


@app.route('/api/retrieve/')
def api_retrieve():
    token = request.args.get('token')
    if not token:
        return "Need valid google oauth token"

    tags = request.args.getlist('tags')
    return jsonify({'vids': datastore.retrieve(token, tags=tags)})


@app.route('/api/store/')
def api_store():
    token = request.args.get('token')
    if not token:
        return "Need valid google oauth token"

    url = request.args.get('url')
    tags = request.args.getlist('tags')
    if not url:
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


@app.route('/api/delete/')
def api_delete():
    token = request.args.get('token')
    if not token:
        return "Need valid google oauth token"

    url = request.args.get('url')

    if not url:
        return "need url parameter"
    return str(datastore.delete(token, url))


@app.route("/")
def index():
    return "Nothing to see here"


@app.route("/dropbox")
def dropbox_export():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
