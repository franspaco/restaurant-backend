from project.db import get_db
from bson import json_util
from project.sessions import create_session

# Kinds:
# 1 - Admin
# 2 - Owner
# 3 - Chef
# 4 - Waiter
# 5 - Costumer

class User:
    def __init__(self, db_user=None):
        if db_user is not None:
            self.id = db_user['_id']
            self.username = db_user['username']
            self.password = db_user['password']
            self.name = db_user['name']
            self.email = db_user['email']
            self.kind = db_user['kind']


    def __str__(self):
        return str(self.id) + " -> " + str(self.username)

    def get_id(self):
        return str(self.id)

    @staticmethod
    def valid_kind(kind):
        return kind >= 1 and kind <= 4

    @staticmethod
    def create(username, password, name, email, kind):
        usr = User()
        usr.username = username
        usr.password = password
        usr.name = name
        usr.email = email
        usr.kind = kind
        db = get_db()
        #db = MongoClient('server.local', 27017).restaurants
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

    @staticmethod
    def login(username, password):
        db = get_db()
        cursor = db.users.find({"username":username, "password": password})
        if cursor.count() is 1:
            user = User(cursor[0])
            return create_session(user)
        else:
            return False

    

if __name__ == '__main__':
    print(User.create("franspaco", "1234", "paco", "lol@example.com", 1))
        



