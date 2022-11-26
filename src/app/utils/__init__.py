from jwt import encode
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import json


def generate_token_jwt(payload):
    token = encode(payload, current_app.config["SECRET_KEY"], "HS256")
    return token


def set_new_password():
    password = str(uuid.uuid4()).split('-')[0]
    return generate_password_hash(password)


def validate_password(password_hash, password):
    return check_password_hash(password_hash, password)


def read_validator_schema_for_models(directory, collection):
    try:
        with open(f'src/app/{directory}/{collection}.json', 'r') as f:
            json_object = json.load(f)
            return json_object
    except Exception as excp:
        print("Erro na leitura do json: " + excp)
        return None


def get_domains(results):
    emails = []
    for i in results:
        emails.append(i.get("email"))
    
    domains = []
    for i in emails:
        domain = i[i.index("@"):]
        if domain not in domains:
            domains.append(domain)
    return domains
