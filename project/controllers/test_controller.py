

from flask import Blueprint, request, abort, current_app
from project.db import get_db
from bson import json_util

bp = Blueprint('test', __name__)

@bp.route('/', methods=['Get', 'POST'])
def user_login():
    return "<h1> Hello world! </h1>"