import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


class Development(object):
    TESTING = False
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')


class Testing(object):
    TESTING = True
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')


app_config = {
    "development" : Development,
    "testing": Testing
}
