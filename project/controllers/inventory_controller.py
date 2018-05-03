
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.inventory import Item
from project.helpers import req_helper
from bson import json_util
from project.db import get_db
import datetime

bp = Blueprint('inventory', __name__)


@bp.route('/create', methods=['POST'])
def inventory_create():
    user = req_helper.force_session_get_user()
    if not user.canEditInventory():
        req_helper.throw_not_allowed()
    data = req_helper.force_json_key_list('material-id', 'expiration-date', 'size')

    date = req_helper.validate_date_format(data['expiration-date'])

    if date < datetime.datetime.now():
        req_helper.throw_operation_failed("Cannot add expired items!")

    item = Item.create(data['material-id'], data['expiration-date'], data['size'])

    if not item:
        req_helper.throw_operation_failed()
    else:
        return jsonify(message="Ok!", id=str(item.id))


