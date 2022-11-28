from bson import json_util
from flask import Blueprint
from flask.wrappers import Response
from src.app.services import get_contacts_exists, get_emails_contact
from src.app.utils import get_domains


contacts = Blueprint("contacts", __name__,  url_prefix="/contacts")


@contacts.route("/<id_user>", methods=["GET"])
def contacts_list(id_user):
    try:
        results = get_contacts_exists(id_user)
    except Exception as exp:
        return Response(
        response=json_util.dumps({"erro": "Não foi possível acessar este ID ou usuário não existe"}),
        status=400,
        mimetype="application/json",
    )

    return Response(
        response=json_util.dumps({"results": results}),
        status=200,
        mimetype="application/json",
    )


@contacts.route("/domain/<id_user>", methods=["GET"])
def domain_list(id_user):
    try:
        results = get_emails_contact(id_user)

        domains = get_domains(results)
    except Exception as exp:
        return Response(
        response=json_util.dumps({"erro": "Não foi possível acessar este ID ou usuário não existe"}),
        status=400,
        mimetype="application/json",
    )

    return Response(
        response=json_util.dumps({"domains": domains}),
        status=200,
        mimetype="application/json",
    )
