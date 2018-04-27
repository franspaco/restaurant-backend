
from flask import Blueprint, request, abort, current_app
from project.db import get_db
from bson.json_util import dumps

bp = Blueprint('user', __name__)

@bp.route('/user/login', methods=['POST'])
def user_login():
    if request.json['username'] and request.json['password']:
        db = get_db()
        cursor = db.users.find({"username":request.json['username'], "password": request.json['password']})
        if cursor.count() is 1:
            return "ok"
            #TODO: generate token
        else:
            abort(400)
    else:
        abort(400)
