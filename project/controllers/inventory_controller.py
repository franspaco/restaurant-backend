
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.material import Material
from project.helpers import req_helper
from bson import json_util
from project.db import get_db

bp = Blueprint('inventory', __name__)