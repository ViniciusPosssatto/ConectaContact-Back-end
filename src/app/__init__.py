import certifi
import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from src.app.config import app_config
from src.app.models import create_collection_users_login, create_collection_contacts


mongo = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsCAFile=certifi.where())
mongo_client = mongo["conecta-contact"]


def create_app(environment):

    app = Flask(__name__)
    app.config.from_object(app_config[environment])
    CORS(app)
 
    mongo_client = mongo["conecta-contact"]
    create_collection_contacts(mongo_client=mongo_client)
    create_collection_users_login(mongo_client=mongo_client)
  
    return app
