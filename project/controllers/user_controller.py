
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.user import User
from project.helpers import req_helper

bp = Blueprint('user', __name__)

@bp.route('/login', methods=['POST'])
def user_login():
    data = req_helper.force_json_key_list('username', 'password')
    token, user = User.login(data['username'], data['password'])
    if token:
        return jsonify(token=token, kind=user.kind)
    else:
        abort(make_response(jsonify(message="Incorrect login!"), 400)) 

@bp.route('/logout', methods=['POST'])
def user_logout():
    usr = req_helper.force_session_get_user()
    usr.logout()
    return "Ok!"

@bp.route('/create', methods=['POST'])
def user_create():
    data = req_helper.force_json_key_list('username', 'password', 'email', 'name', 'kind')
    
    # If trying to create a non-costumer without token
    if data['kind'] is not User.COSTUMER:
        if 'token' not in data:
            abort(make_response(jsonify(message="Missing token!"), 403))
        usr = User.usr_from_token(data['token'])
        # if token is not valid or user cannot create users
        if not usr or not usr.canCreateUsers():
            abort(make_response(jsonify(message="Invalid token!"), 403))

    user = User.create(data['username'], data['password'], data['email'], data['name'], data['kind'])
    if user:
        return jsonify(message="Ok!", id=user.get_id())
    else:
        abort(make_response(jsonify(message="Username taken or invalid kind!"), 400))

