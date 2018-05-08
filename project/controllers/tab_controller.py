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

@bp.route('/all', methods=['POST'])
def tab_all():
    user = req_helper.force_session_get_user()
    if not user.is_staff():
        req_helper.throw_not_allowed()
    out = [tab.toDict() for tab in Tab.query()]
    return jsonify(out)

    

@bp.route('/mytabs', methods=['POST'])
def tabs_get_by_user():
    user = req_helper.force_session_get_user()
    if user.is_staff():
        results = Tab.get_waiter_tabs(user.id)
    else:
        results = Tab.get_customer_tabs(user.id)
    out = [tab.toDict() for tab in results]
    return jsonify(out)


@bp.route('/orders', methods=['POST'])
def get_orders():
    user = req_helper.force_session_get_user()
    if not user.is_staff():
        req_helper.throw_not_allowed()
    
    if user.is_waiter():
        # Get ready
        out = Tab.get_orders(1)
    elif user.is_cook():
        # Get unready
        out = Tab.get_orders(0)
    else:
        # Get all
        out = Tab.get_orders()
    return jsonify(out)


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
def tab_add_order(tab_id):
    user = req_helper.force_session_get_user()
    tab = Tab.tab_from_id(tab_id)

    data = req_helper.force_json_key_list('recipe-id')

    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")

    if not user.canEditTabs() and (user.id not in [val['id'] for val in tab.customers]):
        req_helper.throw_not_allowed(f"You're not allowed to add orders to tab {tab_id}.")

    out = tab.addOrder(data['recipe-id'])
    # Weird thing to make sure it catches only a False and not a 0
    if not(out is False):
        return jsonify(message="Ok!", time=out)
    else:
        req_helper.throw_operation_failed("Failed to add order!")


@bp.route('/<tab_id>/dispatch/<order_id>', methods=['POST'])
def tab_dispatch_order(tab_id, order_id):
    user = req_helper.force_session_get_user()
    if not user.is_staff():
        req_helper.throw_not_allowed()
    # Look for tab and abort if not found
    tab = Tab.tab_from_id(tab_id)
    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")

    order = tab.get_order(order_id)

    if order is None:
        req_helper.throw_not_found("The order id was not found in this tab.")

    if order['status'] == Tab.Order.SERVED:
        req_helper.throw_operation_failed("This order has already reached the last status.")

    if user.is_cook():
        if order['status'] == 0:
            result = tab.dispatch(order_id)
        else:
            req_helper.throw_operation_failed("A cook cannot do this.")
    elif user.is_waiter():
        if order['status'] == 1:
            result = tab.dispatch(order_id)
        else:
            req_helper.throw_operation_failed("A cook cannot do this.")
    else:
        result = tab.dispatch(order_id)

    if result:
        return jsonify(message='Ok!', new_status=order['status']+1)
    else:
        req_helper.throw_operation_failed("Failed to dispatch order!")


@bp.route('/<tab_id>/total', methods=['POST'])
def tab_total(tab_id):
    user = req_helper.force_session_get_user()
    tab = Tab.tab_from_id(tab_id)
    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")
    
    if not user.canEditTabs() and (user.id not in [val['id'] for val in tab.customers]):
        req_helper.throw_not_allowed(f"You're not allowed to view tab {tab_id}.")

    return jsonify(total=tab.get_total())


@bp.route('/<tab_id>/close', methods=['POST'])
def tab_close(tab_id):
    user = req_helper.force_session_get_user()
    if not user.is_staff():
        req_helper.throw_not_allowed()
    tab = Tab.tab_from_id(tab_id)
    if not tab:
        req_helper.throw_not_found("Specified tab could not be found!")
    if tab.close():
        return jsonify(message="Ok!")
    else:
        req_helper.throw_operation_failed("Failed to delete tab!")
