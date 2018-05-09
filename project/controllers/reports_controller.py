from flask import Blueprint, request, abort, make_response, jsonify
from project.models.reports import InventoryReport, TabReport
from project.helpers import req_helper
from bson import json_util
from project.db import get_db
import datetime

bp = Blueprint('reports', __name__)


@bp.route('/inventory/usage', methods=['POST'], strict_slashes=False)
@bp.route('/inventory/usage/<int:days>', methods=['POST'])
def reports_usage_inventory(days=1):
    user = req_helper.force_session_get_user()
    if not user.is_management():
        req_helper.throw_not_allowed()
    return jsonify(data=InventoryReport.usage_pie_chart_report(days))


@bp.route('/inventory/expense', methods=['POST'], strict_slashes=False)
@bp.route('/inventory/expense/<int:days>', methods=['POST'])
def reports_expense_inventory(days=1):
    user = req_helper.force_session_get_user()
    if not user.is_management():
        req_helper.throw_not_allowed()
    return jsonify(data=InventoryReport.expense_pie_chart_report(days))


@bp.route('/customer/tabs', methods=['POST'])
def reports_customer():
    user = req_helper.force_session_get_user()
    if not user.is_customer():
        req_helper.throw_not_allowed("You are not a customer, duh!")
    return jsonify(data=TabReport.customer_pie_chart_report(user.id))



    