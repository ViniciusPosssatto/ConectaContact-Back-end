import os
import json
from flask import Blueprint
from flask.globals import session
from flask.wrappers import Response
from google_auth_oauthlib.flow import Flow


login = Blueprint("login", __name__,  url_prefix="/login")


@login.route("/auth/google", methods=["POST"])
def auth_google():
    
    return Response(
          response=json.dumps({"url": "Funcionando"}),
          status=200,
          mimetype="application/json",
        )