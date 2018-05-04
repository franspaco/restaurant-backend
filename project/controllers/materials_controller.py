
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.material import Material
from project.helpers import req_helper
from bson import json_util
from project.db import get_db


bp = Blueprint('materials', __name__)

@bp.route('/all', methods=['POST'])
def materials_all():
    usr = req_helper.force_session_get_user()
    if usr.is_costumer():
        req_helper.throw_not_allowed()
    materials = Material.query_materials()
    return jsonify(materials)

@bp.route('/find', methods=['POST'])
def material_find():
    req_helper.force_session_get_user()
    data = req_helper.force_json_key_list('material-id')

    mat = Material.get_from_id(data['material-id'])

    if mat:
        return jsonify(mat.__dict__)
    else:
        req_helper.throw_not_found("Material not found!")

@bp.route('/create', methods=['POST'])
def material_create():
    usr = req_helper.force_session_get_user()
    if not usr.canCreateMaterials():
        abort(make_response(jsonify(message="Cannot create materials"), 403))
    
    data = req_helper.force_json_key_list('name', 'img_url', 'units')

    if (data['units'] != 'mL') and (data['units'] != 'g'):
        req_helper.throw_operation_failed("Invalid units! Use 'mL' or 'g'")

    mat = Material.create(data['name'], data['img_url'], data['units'])
    return jsonify(message="Success!", id=mat.get_id())
    