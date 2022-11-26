from src.app.utils import read_validator_schema_for_models


def create_collection_users_login(mongo_client):
	users_login_validator = read_validator_schema_for_models("schemas", "user_login_schema")

	try:
		mongo_client.create_collection("users_login")
	except Exception as e:
		print({"msg": e})

	mongo_client.command("collMod", "users_login", validator=users_login_validator)


def create_collection_contacts(mongo_client):

	contacts_validator = read_validator_schema_for_models("schemas", "contacts_schema")

	try:
		mongo_client.create_collection("contacts")
	except Exception as e:
		print({"msg": e})

	mongo_client.command("collMod", "contacts", validator=contacts_validator)
