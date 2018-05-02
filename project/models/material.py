
from project.db import get_db
import json

class Material:

    def get_id(self):
        return str(self.id)

    @staticmethod
    def create(name, img_url):
        material = Material()
        material.name = name
        material.img_url = img_url
        db = get_db()

        id = db.materials.insert({
            "name": name,
            "img_url": img_url
        })
        material.id = id
        return material
