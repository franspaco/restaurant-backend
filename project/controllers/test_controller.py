

from flask import Blueprint, request, abort, make_response, send_file
from project.db import get_db, load_kv, save_kv
from project.models .user import User
from bson import json_util

bp = Blueprint('test', __name__)

@bp.route('/', methods=['Get', 'POST'])
def test():
    return "<h1> Hello world! </h1>"

@bp.route('/dope')
def wat():
    abort(make_response("Lol", 420))

@bp.route('/init', methods=['GET'])
def init_form():
    setup = load_kv('setup')
    if setup:
        abort(make_response("APP HAS ALREADY BEEN INITIALIZED!", 403))
    return send_file("static/setup.html")

@bp.route('/init', methods=['POST'])
def init_post():
    data = request.form
    if data is None:
        abort(make_response("INVALID DATA", 400))
    keys = ['username', 'password', 'name', 'email', 'tables']
    for key in keys:
        if key not in data:
            abort(make_response("Missing: " + key, 400))

    try:
        tables = int(data['tables'])
    except ValueError:
        abort(make_response("Tables must be an int!", 400))

    res = User.create(data['username'], data['password'], data['name'], data['email'], 1)

    if res:
        save_kv('tables', tables)
        save_kv('setup', True)
        return "<h1>System is ready</h1>Admin is: " + data['username']
    else:
        return "<h1>Setup failed!</h1>Try again!"