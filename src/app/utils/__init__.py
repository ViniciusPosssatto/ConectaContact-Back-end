from jwt import encode
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
import uuid


def generate_token_jwt(payload):
    token = encode(payload, current_app.config["SECRET_KEY"], "HS256")
    return token


def set_new_password():
    password = str(uuid.uuid4()).split('-')[0]
    return generate_password_hash(password)


def validate_password(password_hash, password):
    return check_password_hash(password_hash, password)
