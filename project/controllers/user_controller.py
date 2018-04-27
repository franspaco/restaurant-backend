
from flask import Blueprint, request, abort, current_app, make_response, jsonify
from project.db import get_db
from bson.json_util import dumps
from project.models.user import User

bp = Blueprint('user', __name__)

@bp.route('/login', methods=['POST'])
def user_login():
    if request.json['username'] and request.json['password']:
        token = User.login(request.json['username'], request.json['password'])
        if token:
            return jsonify(token=token)
        else:
           abort(make_response(jsonify(message="Incorrect login!"), 400)) 
    else:
        abort(make_response(jsonify(message="Missing data!"), 400))

@bp.route('/create', methods=['POST'])
def user_create():
    data = request.json
    if data is not None and 'username' in data and 'password' in data and 'email' in data and 'name' in data and 'kind' in data:
        user = User.create(data['username'], data['password'], data['email'], data['name'], data['kind'])
        if user:
            return jsonify(message="Ok!", id=user.get_id())
        else:
            abort(make_response(jsonify(message="Username taken!"), 400))
    else:
        abort(make_response(jsonify(message="Missing data!"), 400))

