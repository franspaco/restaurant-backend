

from flask import Blueprint, request, abort, current_app, make_response
from project.db import get_db
from bson import json_util

bp = Blueprint('test', __name__)

@bp.route('/', methods=['Get', 'POST'])
def test():
    return "<h1> Hello world! </h1>"

@bp.route('/dope')
def wat():
    abort(make_response("Lol", 420))