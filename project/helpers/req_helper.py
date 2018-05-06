
from flask import request, abort, current_app, make_response, jsonify
from project.models.user import User
import datetime

"""
    Make sure a token is provided and it's related to a valid session.
    Otherwise abort.
    Returns the user if successful
"""
def force_session_get_user():
    data = request.json
    if data is not None and 'token' in data:
        usr = User.usr_from_token(data['token'])
        if usr:
            return usr
    abort(make_response(jsonify(message="Please log in to do this!"), 403))

""" 
    Make sure all the requested keys are in the JSON request.
    Aborts if parameter is missing.
    Returns the json object
"""
def force_json_key_list(*args):
    data = request.json
    if data is None:
        abort(make_response(jsonify(message="No JSON provided!"), 400))
    for arg in args:
        if arg not in data:
            abort(make_response(jsonify(message="Missing data!", debug=f"Key not found: '{arg}'"), 400))
    return data

def get_optional_key(key, default=None, force_instance=False):
    if key in request.json:
        if force_instance:
            if isinstance(request.json[key], type(default)):
                return request.json[key]
            else:
                return default
        else:
            return request.json[key]
    else:
         return default

def json_dump(object):
    object['id'] = str(object['_id'])
    object.pop('_id', None)
    return jsonify(object)

def throw_operation_failed(msg="Operation failed!"):
    abort(make_response(jsonify(message=msg), 400))

def throw_not_allowed(msg="Insufficient permissions!"):
    abort(make_response(jsonify(message=msg), 403))

def throw_not_found(msg="Could not find the requested object!"):
    abort(make_response(jsonify(message=msg), 404))

def throw_teapot(msg="Well... this is awkward."):
    abort(make_response(jsonify(message=msg), 418))

def validate_date_format(data):
    try:
        return datetime.datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        abort(make_response(jsonify(message="Invalid date format! Use YYYY-MM-DD"), 400))