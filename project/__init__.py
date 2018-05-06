import os
from flask import Flask

app = Flask(__name__)

from project.controllers import user_controller, test_controller, materials_controller
from project.controllers import inventory_controller, recipe_controller, tab_controller
from project.controllers import tables_controller

app.register_blueprint(test_controller.bp)
app.register_blueprint(user_controller.bp, url_prefix='/user')
app.register_blueprint(materials_controller.bp, url_prefix='/material')
app.register_blueprint(inventory_controller.bp, url_prefix='/inventory')
app.register_blueprint(recipe_controller.bp, url_prefix='/recipe')
app.register_blueprint(tab_controller.bp, url_prefix='/tab')
app.register_blueprint(tables_controller.bp, url_prefix='/tables')