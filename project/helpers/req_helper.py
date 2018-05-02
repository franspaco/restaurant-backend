
from flask import request, abort, current_app, make_response, jsonify
from project.models.user import User

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
            abort(make_response(jsonify(message="Missing data!"), 400))
    
    return data