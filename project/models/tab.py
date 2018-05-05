
from project.db import get_db
from project.models.user import User
from bson import ObjectId

class Tab:

    def __init__(self, db_tab=None):
        if db_tab is not None:
            self.id = str(db_tab['_id'])
            self.waiter = db_tab['waiter']
            self.table = db_tab['table']
            self.customers = db_tab['customers']
            self.orders = db_tab['orders']
            pass

    def toDict(self):
        return self.__dict__
    
    @staticmethod
    def create(waiter_usr, table_no, creation_time, customers=None):

        customer_list = list()

        if isinstance(customers, list):
            for val in customers:
                usr = User.user_from_username(val)
                if not usr:
                    return False
                print(usr.name)
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
            "customers": customer_list,
            "orders": list()
        })

        return str(id)

    @staticmethod
    def tab_from_id(id):
        try:
            _id = ObjectId(id)
        except:
            return False
        
        result = get_db().tabs.find_one({'_id':_id})

        if result is not None:
            return Tab(result)
        else:
            return False