
from project.db import get_db
from project.models.user import User

class Tab:

    def __init__(self, db_tab=None):
        if db_tab is not None:
            #TODO: this
            pass
    
    @staticmethod
    def create(waiter_usr, table_no, creation_time, customers=None):

        customer_list = list()

        if isinstance(customers, list):
            for val in customers:
                usr = User.user_from_username(val)
                if not usr:
                    return False
                customer_list.append({
                    "id": usr.id,
                    "name": usr.name,
                    "username": usr.username
                })

        id = get_db().tabs.insert({
            'waiter':{
                'id': waiter_usr.id,
                'name': waiter_usr.name
            },
            "table": table_no,
            "registration": creation_time,
            "customers": customer_list
        })

        return id