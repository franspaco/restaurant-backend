from flask import Blueprint, request, abort, make_response, jsonify
from project.models.reports import InventoryReport, TabReport
from project.helpers import req_helper
from bson import json_util
from project.db import get_db
import datetime

bp = Blueprint('reports', __name__)


@bp.route('/inventory', methods=['POST'], defaults={'days':1}, strict_slashes=False)
@bp.route('/inventory/<days>', methods=['POST'])
def reports_inventory(days):
    user = req_helper.force_session_get_user()
    if not user.is_management():
        req_helper.throw_not_allowed()
    
    return jsonify(data=InventoryReport.pie_chart_report(days))

@bp.route('/cutomer', methods=['POST'])
def reports_customer():
    user = req_helper.force_session_get_user()
    if not user.is_management():
        req_helper.throw_not_allowed()
    
    return jsonify(data=TabReport.pie_chart_report(user.id))



    