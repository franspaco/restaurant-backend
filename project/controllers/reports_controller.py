from flask import Blueprint, request, abort, make_response, jsonify
from project.models.inventory import Item
from project.helpers import req_helper
from bson import json_util
from project.db import get_db
import datetime

bp = Blueprint('reports', __name__)

@bp.route('/inv', methods=['POST'])
def reports_inventory():
    user = req_helper.force_session_get_user()
    if not user.is_management():
        req_helper.throw_not_allowed()
    
    return jsonify(data=Item.pie_chart_report())

    