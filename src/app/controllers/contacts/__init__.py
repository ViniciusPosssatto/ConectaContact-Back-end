import json
import requests
from bson import json_util, ObjectId
from flask import Blueprint
from flask.wrappers import Response
from src.app import mongo_client



contacts = Blueprint("contacts", __name__,  url_prefix="/contacts")


@contacts.route("/<id_user>", methods=["GET"])
def contacts_list(id_user):

    results = mongo_client.contacts.find({"id_user": ObjectId(id_user)})

    return Response(
        response=json_util.dumps({"results": results}),
        status=200,
        mimetype="application/json",
    )
