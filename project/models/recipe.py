
from project.db import get_db
from project.models.material import Material

class Recipe:

    def __init__(self, db_recipe=None):
        if db_recipe is not None:
            self.id = str(db_recipe['_id'])
            self.name = db_recipe['name']
            self.desc = db_recipe['desc']
            self.detail = db_recipe['detail']
            self.img_url = db_recipe['img_url']
            self.cost = db_recipe['cost']
            self.ingredients = db_recipe['ingredients']
            self.src = db_recipe['src']
            self.time= db_recipe['time']

    @staticmethod
    def query(params=None):
        cursor = get_db().recipes.find(params)
        out = list()
        for doc in cursor:
            recipe = Recipe(db_recipe=doc)
            out.append(recipe)
        return out
    
    @staticmethod
    def create(name, desc, detail, img_url, cost, ingredients, src, time):
        in_list = list()

        for val in ingredients:
            mat = Material.get_from_id(val['material-id'])
            if not mat:
                return False
            try: 
                val['quantity'] = int(val['quantity'])
            except:
                return False
            val['name'] = mat.name
            val['units'] = mat.units
            in_list.append(val)

        id = get_db().recipes.insert({
            "name": name,
            "desc": desc,
            "detail": detail,
            "img_url": img_url,
            "cost": cost,
            "ingredients": in_list,
            "src": src,
            "time": time
        })
        return id