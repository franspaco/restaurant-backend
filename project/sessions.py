
from project.db import get_db
from uuid import uuid4

def create_session(user):
    sessions = get_db().sessions
    token = str(uuid4())
    sessions.find_one_and_update({"_id":user.id}, {'$set':{"token": token}}, usert=True)
    return token

def destroy_session(token):
    sessions = get_db().sessions
    return sessions.delete_one({"token":token}).deleted_count