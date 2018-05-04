
from project.db import get_db
from bson import ObjectId
import json

class Material:

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_from_id(id):
        try:
            res = get_db().materials.find_one({'_id':ObjectId(id)})
            if res is not None:
                return res
            else:
                return False
        except:
            return False


    @staticmethod
    def create(name, img_url, units):
        material = Material()
        material.name = name
        material.img_url = img_url
        material.units = units
        db = get_db()

        id = db.materials.insert({
            "name": name,
            "img_url": img_url,
            "units": units
        })
        material.id = id
        return material
