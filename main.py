import os
from flask import Flask, request, abort
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']))

@app.route('/')
def hello_world():
    return 'Woop woop'

@app.route('/db/<collection>')
def get_restaurants(collection):
    cursor = client.test[collection].find({})
    out = list()
    for doc in cursor:
        out.append(doc)
    return dumps(out)

@app.route('/db/<collection>/<obj_id>')
def get_restaurant(collection, obj_id):
    try:
        cursor = client.test[collection].find({"_id": ObjectId(obj_id)})
        if cursor.count() < 1:
            abort(404)
        return dumps(cursor[0])
    except:
        abort(400)

@app.route('/db/<collection>/insert', methods=['POST'])
def put_json(collection):
    content = request.get_json()
    res = client.test[collection].insert(content)
    return dumps(res)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
