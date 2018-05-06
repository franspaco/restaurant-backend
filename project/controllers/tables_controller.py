
from flask import Blueprint, request, abort, make_response, jsonify
from project.db import save_kv, load_kv, get_db
from project.helpers import req_helper

bp = Blueprint('tables', __name__)

@bp.route('/', methods=['POST'])
def tables_get():
    req_helper.force_session_get_user()
    tables = load_kv('tables')
    if tables is not None:
        return jsonify(tables=tables)
    else:
        req_helper.throw_teapot()

@bp.route('/<int:number>', methods=['POST'])
def tables_set(number):
    user = req_helper.force_session_get_user()
    if not user.is_admin():
        req_helper.throw_not_allowed()
    save_kv('tables', number)
    return jsonify(message='Ok!')

@bp.route('/available', methods=['POST'])
def tables_get_available():
    user = req_helper.force_session_get_user()
    if not user.is_admin():
        req_helper.throw_not_allowed()

    tables = load_kv('tables')

    used_tables = get_db().tabs.find().distinct("table")

    available = [ i for i in range(1, tables+1) if i not in used_tables]

    return jsonify(available)

