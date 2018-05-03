from project.db import get_db
from bson import json_util
from project.sessions import create_session, find_session, destroy_all_user_sessions

# Kinds:
# 1 - Admin
# 2 - Owner
# 3 - Chef/Cook
# 4 - Waiter
# 5 - Costumer

class User:

    # kinds/roles
    ADMIN    = 1
    OWNER    = 2
    COOK     = 3
    WAITER   = 4
    COSTUMER = 5

    @staticmethod
    def valid_kind(kind):
        return kind >= User.ADMIN and kind <= User.COSTUMER

    def __init__(self, db_user=None):
        if db_user is not None:
            self.id = db_user['_id']
            self.username = db_user['username']
            self.password = db_user['password']
            self.name = db_user['name']
            self.email = db_user['email']
            self.kind = db_user['kind']


    def __str__(self):
        return str(self.id) + " -> " + str(self.username) + " -> " + str(self.kind)

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.kind == User.ADMIN

    def is_owner(self):
        return self.kind == User.OWNER

    def is_cook(self):
        return self.kind == User.COOK

    def is_waiter(self):
        return self.kind == User.WAITER
    
    def is_costumer(self):
        return self.kind == User.COSTUMER

    def canCreateUsers(self):
        return self.is_admin()

    def canCreateMaterials(self):
        if self.is_admin() or self.is_owner():
            return True
        else:
            return False

    @staticmethod
    def create(username, password, name, email, kind):
        usr = User()
        usr.username = username
        usr.password = password
        usr.name = name
        usr.email = email
        usr.kind = kind

        # Make sure kind is valid
        if not User.valid_kind(kind):
            return False

        db = get_db()
        # Check for reapeated username
        if db.users.find({"username":username}).count() > 0:
            return False

        id = db.users.insert({
            "username":username,
            "password": password,
            "name": name,
            "email": email,
            "kind": kind
        })
        usr.id = id
        return usr

    def logout(self):
        return destroy_all_user_sessions(self.id)

    @staticmethod
    def login(username, password):
        db = get_db()
        cursor = db.users.find({"username":username, "password": password})
        if cursor.count() is 1:
            user = User(cursor[0])
            return create_session(user), user
        else:
            return False, None

    @staticmethod
    def usr_from_token(token):
        db = get_db()
        resid = find_session(token)
        if not resid:
            return False
        cursor = db.users.find({"_id":resid})
        if cursor.count() is 1:
            user = User(cursor[0])
            return user
        else:
            return False

    

if __name__ == '__main__':
    print(User.create("franspaco", "1234", "paco", "lol@example.com", 1))
        



