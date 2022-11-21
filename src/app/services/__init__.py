from bson import ObjectId
from src.app import mongo_client


def insert_user_in_db(new_user):
    mongo_client.users_login.insert_one(new_user)


def get_user_exists(user_email):
    user = mongo_client.users_login.find_one({"email": user_email})
    return user


def get_contacts_exists(id_user):
    results = mongo_client.contacts.find({"id_user": ObjectId(id_user)})
    return results


def verify_and_save_contacts(contacts, id_user):
    for contact in contacts:
        contact_exists =  mongo_client.contacts.find_one({"email": contact.get("email"), "id_user": ObjectId(id_user)})
        if not contact_exists: 
            mongo_client.contacts.insert_one(contact)
