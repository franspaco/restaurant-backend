
from project.db import get_db
from project.models.material import Material

class Item:

    def __init__(self, db_item=None):
        if db_item is not None:
            self.id = str(db_item['_id'])
            self.material = db_item['material']
            self.expiration = db_item['expiration']
            self.size = db_item['size']
            self.arrival = db_item['arrival']
            self.cost = db_item['cost']

    @staticmethod
    def create(material_id, expiration_date, arrival_date, cost, size):
        item = Item()
        item.material = material_id
        item.expiration = expiration_date
        item.size = size
        item.arrival = arrival_date
        item.cost = cost

        if not Material.get_from_id(material_id):
            return False

        db = get_db()

        id = db.inventory.insert({
            "material": material_id,
            "expiration": expiration_date,
            "arrival": arrival_date,
            "size": size,
            "cost": cost
        })
        item.id = str(id)
        return item

    @staticmethod
    def query_items(material=None):
        query = dict()
        if material is not None:
            query['material'] = material
        cursor = get_db().inventory.find(query)
        results = list()
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            results.append(doc)
        return results