
from project.db import get_db
from uuid import uuid4

def create_session(user):
    sessions = get_db().sessions
    token = str(uuid4())
    sessions.replace_one({"_id":user.id}, {"token": token}, upsert=True)
    return token

def destroy_session(token):
    sessions = get_db().sessions
    return sessions.delete_one({"token":token}).deleted_count

def destroy_all_user_sessions(id):
    sessions = get_db().sessions
    return sessions.delete_many({"_id":id}).deleted_count

def find_session(token):
    result = get_db().sessions.find_one({"token":token})
    if result is not None:
        return result['_id']
    else:
        return False