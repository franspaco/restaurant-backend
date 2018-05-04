
from project.db import get_db
from project.models.material import Material

class Item:
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
        item.id = id
        return item