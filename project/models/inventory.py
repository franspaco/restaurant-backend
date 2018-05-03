
from project.db import get_db
from project.models.material import Material

class Item:
    @staticmethod
    def create(material_id, expiration_date, size):
        item = Item()
        item.material = material_id
        item.expiration = expiration_date
        item.size = size

        if not Material.get_from_id(material_id):
            return False

        db = get_db()

        id = db.inventory.insert({
            "material": material_id,
            "expiration": expiration_date,
            "size": size
        })
        item.id = id
        return item