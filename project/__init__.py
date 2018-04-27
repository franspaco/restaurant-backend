import os
from flask import Flask

app = Flask(__name__)

from project.controllers import user_controller

app.register_blueprint(user_controller.bp)