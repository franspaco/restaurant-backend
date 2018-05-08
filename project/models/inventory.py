
from project.db import get_db
from project.models.material import Material
from bson import ObjectId
from datetime import datetime, timedelta

class Item:

    def __init__(self, db_item=None):
        if db_item is not None:
            self.id = str(db_item['_id'])
            self.material = db_item['material']
            self.expiration = db_item['expiration'].strftime('%Y-%m-%d')
            self.size = db_item['size']
            self.arrival = db_item['arrival'].strftime('%Y-%m-%d')
            self.cost = db_item['cost']
            self.location = db_item['location']
            self.expired = db_item['expiration'] <= datetime.today()
            self.material_name = db_item['material_name']
    

    @staticmethod
    def create(material_id, expiration_date, arrival_date, cost, size, location):
        item = Item()
        item.material = material_id
        item.expiration = expiration_date
        item.size = size
        item.arrival = arrival_date
        item.cost = cost

        mat = Material.get_from_id(material_id)
        if not mat:
            return False

        db = get_db()

        id = db.inventory.insert({
            "material": material_id,
            "expiration": expiration_date,
            "arrival": arrival_date,
            "size": size,
            "cost": cost,
            "location": location,
            "material_name": mat.name
        })
        item.id = str(id)
        return item

    @staticmethod
    def get_from_id(id):
        try:
            res = get_db().inventory.find_one({'_id':ObjectId(id)})
        except:
            return False
        if res is not None:
            return Item(db_item=res)
        else:
            return False

    @staticmethod
    def query(params=None):
        cursor = get_db().inventory.find(params)
        out = list()
        for doc in cursor:
            recipe = Item(db_item=doc)
            out.append(recipe)
        return out

    @staticmethod
    def query_items(material=None):
        query = dict()
        if material is not None:
            query['material'] = material
        cursor = get_db().inventory.find(query)
        results = list()
        for doc in cursor:
            results.append(Item(doc))
        return results
    
    def destroy(self):
        res =  get_db().inventory.delete_one({'_id':ObjectId(self.id)})
        if res.deleted_count == 1:
            item_dict = self.__dict__
            item_dict['arrival'] = datetime.strptime(self.arrival, '%Y-%m-%d')
            item_dict['expiration'] = datetime.strptime(self.expiration, '%Y-%m-%d')
            item_dict['checkout_time'] = datetime.now()
            get_db().inventory_log.insert(item_dict)
            return True
        else:
            return False

    @staticmethod
    def pie_chart_report():
        pipeline = [
            {
                '$match':{
                    'checkout_time':{
                        '$gt': datetime.now() - timedelta(days=1)
                    }
                }
            },
            {
                '$group':{
                    '_id': '$material_name',
                    'count':{ '$sum':1},
                    'total': { '$sum': '$cost'}
                }
            },
            {
                '$project':{
                    '_id':0,
                    'name':'$_id',
                    'count':1,
                    'total':1
                }
            }
        ]
        cursor = get_db().inventory_log.aggregate(pipeline)
        return [doc for doc in cursor]