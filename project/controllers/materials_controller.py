
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.material import Material
from project.helpers import req_helper
from bson import json_util
from project.db import get_db


bp = Blueprint('materials', __name__)

@bp.route('/all')
def materials_all():
    db = get_db()
    cursor = db.materials.find()
    materials = list()
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        materials.append(doc)
    return json_util.dumps(materials)

@bp.route('/create', methods=['POST'])
def material_create():
    usr = req_helper.force_session_get_user()
    if not usr.canCreateMaterials():
        abort(make_response(jsonify(message="Cannot create materials"), 403))
    
    data = req_helper.force_json_key_list('name', 'img_url')
    mat = Material.create(data['name'], data['img_url'])
    return jsonify(message="Success!", id=mat.get_id())
    