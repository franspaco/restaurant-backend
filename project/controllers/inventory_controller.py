
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
    data = req_helper.force_json_key_list('material-id', 'expiration-date', 'size', 'cost')
    expiration_date = req_helper.validate_date_format(data['expiration-date'])
    if expiration_date < datetime.datetime.now():
        req_helper.throw_operation_failed("Cannot add expired items!")

    amount = req_helper.get_optional_key('amount', 1)

    try:
        amount = int(amount)
    except:
        req_helper.throw_operation_failed("Boi, that amount is not a number!")

    if amount < 1:
        req_helper.throw_operation_failed("Boi, don't send negative/zero amounts!")

    cost = data['cost']/amount
    today = datetime.datetime.today()

    for _ in range(amount):
        item = Item.create(data['material-id'], expiration_date, today, cost, data['size'])
        #if error
        if not item:
            req_helper.throw_operation_failed("Could not create! Maybe check the material-id.")

    return jsonify(message="Ok!", id=str(item.id))


@bp.route('/query', methods=['POST'], defaults={'material_id':None}, strict_slashes=False)
@bp.route('/query/<material_id>', methods=['POST'])
def inventory_query(material_id):
    user = req_helper.force_session_get_user()
    if not user.canEditInventory():
        req_helper.throw_not_allowed()
    
    result = Item.query_items(material_id)

    return jsonify(result)


