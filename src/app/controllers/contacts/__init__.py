from bson import json_util
from flask import Blueprint
from flask.wrappers import Response
from src.app.services import get_contacts_exists


contacts = Blueprint("contacts", __name__,  url_prefix="/contacts")


@contacts.route("/<id_user>", methods=["GET"])
def contacts_list(id_user):

    results = get_contacts_exists(id_user)

    return Response(
        response=json_util.dumps({"results": results}),
        status=200,
        mimetype="application/json",
    )
