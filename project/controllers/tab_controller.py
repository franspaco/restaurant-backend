
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.tab import Tab
from project.helpers import req_helper
from datetime import datetime

bp = Blueprint('tab', __name__)

@bp.route('/create', methods=['POST'])
def tab_create():
    user = req_helper.force_session_get_user()
    if not user.canEditTabs():
        req_helper.throw_not_allowed()
    
    data = req_helper.force_json_key_list('table')

    try:
        table = int(data['table'])
    except:
        req_helper.throw_operation_failed("Table must be an integer")

    if 'customers' in data and isinstance(data['customers'], list) and len(data['customers']) > 0:
        customers = data['customers']
    else:
        customers = None

    tab_id = Tab.create(user, table, datetime.now(), customers)

    if not tab_id:
        req_helper.throw_operation_failed("Could not create! Maybe check usernames!")
    else:
        return jsonify(message='Ok!', id=tab_id)

@bp.route('/<tab_id>', methods=['POST'])
def tab_preview(tab_id):
    user = req_helper.force_session_get_user()
    tab = Tab.tab_from_id(tab_id)

    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")

    if not user.canEditTabs() and (user.id not in [val['id'] for val in tab.customers]):
        req_helper.throw_not_allowed(f"You're not allowed to view tab {tab_id}.")
    
    return jsonify(tab.toDict())


@bp.route('/<tab_id>/addcustomer', methods=['POST'])
def tab_add_customer(tab_id):
    user = req_helper.force_session_get_user()
    tab = Tab.tab_from_id(tab_id)

    data = req_helper.force_json_key_list('username')

    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")

    if not user.canEditTabs() and (user.id not in [val['id'] for val in tab.customers]):
        req_helper.throw_not_allowed(f"You're not allowed to add costumers to tab {tab_id}.")

    if tab.addCustomer(data['username']):
        return jsonify(message="Ok!")
    else:
        req_helper.throw_operation_failed("Failed to add user!")

@bp.route('/<tab_id>/addorder', methods=['POST'])
def tabb_add_order(tab_id):
    user = req_helper.force_session_get_user()
    tab = Tab.tab_from_id(tab_id)

    data = req_helper.force_json_key_list('username')

    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")