import datastore

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return str(datastore.mongo_test())

if __name__ == "__main__":
    app.run()

