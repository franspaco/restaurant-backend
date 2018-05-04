
from project.db import get_db
from bson import ObjectId
import json

class Material:

    def __init__(self, db_material=None):
        if db_material is not None:
            self.id = str(db_material['_id'])
            self.name = db_material['name']
            self.img_url = db_material['img_url']
            self.units = db_material['units']

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_from_id(id):
        try:
            res = get_db().materials.find_one({'_id':ObjectId(id)})
            print(res)
            if res is not None:
                return Material(db_material=res)
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

    @staticmethod
    def query_materials(remove=[]):
        cursor = get_db().materials.find()
        results = list()
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            for key in remove:
                doc.pop(key, None)
            results.append(doc)
        return results
