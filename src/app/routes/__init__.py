from flask import Flask
from src.app.controllers.login import login


def routes(app: Flask):
    app.register_blueprint(login)
