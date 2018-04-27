import os
from flask import Flask

app = Flask(__name__)

from project.controllers import user_controller, test_controller

app.register_blueprint(test_controller.bp)
app.register_blueprint(user_controller.bp, url_prefix='/user')