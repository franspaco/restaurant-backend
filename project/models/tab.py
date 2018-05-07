
from project.db import get_db
from project.models.user import User
from project.models.recipe import Recipe
from bson import ObjectId
from datetime import datetime, timedelta

class Tab:

    class Order:
        ORDERED = 0
        READY = 1
        SERVED = 2

    def __init__(self, db_tab=None):
        if db_tab is not None:
            self.id = str(db_tab['_id'])
            self.waiter = db_tab['waiter']
            self.table = db_tab['table']
            self.customers = db_tab['customers']
            self.orders = db_tab['orders']

    def toDict(self):
        return self.__dict__

    def addCustomer(self, username):
        usr = User.user_from_username(username)
        if not usr:
            return False
        
        # Check for uniqueness
        if usr.id in [val['id'] for val in self.customers]:
            return False

        new_data = {
            "id": usr.id,
            "name": usr.name,
            "username": usr.username
        }
        self.customers.append(new_data)
        result = get_db().tabs.update_one({'_id':ObjectId(self.id)},{'$push':{'customers':new_data}})
        if result.modified_count == 1:
            return True
        else:
            return False

    def addOrder(self, recipe_id):
        recipe = Recipe.query_id(recipe_id)

        if recipe is None:
            return False

        new_data = {
            'id': str(ObjectId()),
            'recipe-id': recipe.id,
            'name': recipe.name,
            'img_url': recipe.img_url,
            'cost': recipe.cost,
            'category': recipe.category,
            'order-time': datetime.now().isoformat(),
            'eta': (datetime.now() + timedelta(minutes=recipe.time)).isoformat(),
            'status': 0,
            'tab-id': self.id
        }
        self.orders.append(new_data)
        result = get_db().tabs.update_one({'_id': ObjectId(self.id)}, {'$push': {'orders': new_data}})
        if result.modified_count == 1:
            return True
        else:
            return False

    def get_order(self, id):
        for order in self.orders:
            print(f"{order['id']} vs {id}")
            if order['id'] == id:
                print("Match!!")
                return order
        return None

    def dispatch(self, order_id):
        order = self.get_order(order_id)
        if order is None:
            return False
        result = get_db().tabs.update_one(
            {
                '_id':ObjectId(self.id), 
                'orders.id':order['id']
            }, 
            {
                '$inc':{
                    'orders.$.status':1
                }
            }
        )
        if result.modified_count == 1:
            return True
        else:
            return False


    @staticmethod
    def create(waiter_usr, table_no, creation_time, customers=None):

        customer_list = list()

        if isinstance(customers, list):
            customers = list(set(customers))
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


    @staticmethod
    def query(params=None):
        cursor = get_db().tabs.find(params)
        out = list()
        for doc in cursor:
            out.append(Tab(db_tab=doc))
        return out


    @staticmethod
    def get_waiter_tabs(uid):
        return Tab.query({'waiter.id': uid})


    @staticmethod
    def get_customer_tabs(uid):
        return Tab.query({'customers.id': uid})


    @staticmethod
    def get_orders(status=None):
        if status is not None:
            status = {"orders.status":status}
        else:
            status = {}
        pipeline = [
            {"$unwind":"$orders"},
            {'$match':status},
            {'$replaceRoot':{'newRoot':'$orders'}}
        ]
        cursor = get_db().tabs.aggregate(pipeline)
        return [doc for doc in cursor]