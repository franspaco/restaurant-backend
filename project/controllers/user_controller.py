
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
        if not usr or not usr.canEditUsers():
            abort(make_response(jsonify(message="Invalid token!"), 403))

    if not data['username'].strip():
        req_helper.throw_operation_failed("Username empty!")

    if not data['password'].strip() or len(data['password']) < 4:
        req_helper.throw_operation_failed("Password empty or shorter than 4 chars!")

    user = User.create(data['username'], data['password'], data['email'], data['name'], data['kind'])
    if user:
        return jsonify(message="Ok!", id=user.get_id())
    else:
        abort(make_response(jsonify(message="Username taken or invalid kind!"), 400))

@bp.route('/query', methods=['POST'], defaults={'kind':None}, strict_slashes=False)
@bp.route('/query/<int:kind>', methods=['POST'])
def user_query_type(kind):
    usr = req_helper.force_session_get_user()
    if not usr.is_admin():
        req_helper.throw_not_allowed()
    
    if kind is not None and not User.valid_kind(kind):
        req_helper.throw_operation_failed("Invalid type!")

    users = User.query_users(kind=kind, remove=['password'])

    return jsonify(users)

@bp.route('/delete', methods=['DELETE'])
def user_delete():
    usr = req_helper.force_session_get_user()
    if not usr.canEditUsers():
        req_helper.throw_not_allowed()

    data = req_helper.force_json_key_list('user-id')
    
    user = User.get_from_id(data['user-id'])

    if not user:
        req_helper.throw_not_found("User not found!")

    user.logout()
    if user.destroy() == 1:
        return jsonify(message="Ok!")
    else:
        req_helper.throw_operation_failed()
    