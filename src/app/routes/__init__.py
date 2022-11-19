from flask import Flask
from src.app.controllers import login


def routes(app: Flask):
    app.register_blueprint(login)
