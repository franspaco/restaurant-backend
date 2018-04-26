
from flask import Flask, request, abort
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

@app.route('/')
def hello_world():
    return 'Woop woop'

@app.route('/restaurants')
def get_restaurants():
    cursor = client.test.restaurants.find({})
    out = list()
    for doc in cursor:
        out.append(doc)
    return dumps(out)

@app.route('/restaurant/<obj_id>')
def get_restaurant(obj_id):
    try:
        cursor = client.test.restaurants.find({"_id": ObjectId(obj_id)})
        if cursor.count() < 1:
            abort(404)
        return dumps(cursor[0])
    except:
        abort(400)

@app.route('/json', methods=['POST'])
def put_json():
    content = request.get_json()
    return dumps(content)
