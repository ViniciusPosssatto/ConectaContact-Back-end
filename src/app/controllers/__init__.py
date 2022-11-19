import os
import json
from flask import Blueprint
from flask.globals import session
from flask.wrappers import Response
from google_auth_oauthlib.flow import Flow


login = Blueprint("login", __name__,  url_prefix="/login")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file="src\\app\\utils\\client_secret.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ],
    redirect_uri="http://localhost:5000/login/callback",
)


@login.route("/auth/google", methods=["POST"])
def auth_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return Response(
		response=json.dumps({"url": authorization_url}),
		status=200,
		mimetype="application/json",
        )
