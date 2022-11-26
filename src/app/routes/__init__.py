from flask import Flask
from src.app.controllers.login import login
from src.app.controllers.contacts import contacts


def routes(app: Flask):
    app.register_blueprint(login)
    app.register_blueprint(contacts)
