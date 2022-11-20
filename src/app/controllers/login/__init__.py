import os
import json
import requests
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app
from flask.globals import session
from flask.wrappers import Response
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google import auth
from werkzeug.utils import redirect
from src.app.utils import generate_token_jwt, set_new_password
from src.app import mongo_client
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


login = Blueprint("login", __name__,  url_prefix="/login")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file="src\\app\\utils\\client_secret.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
		"https://www.googleapis.com/auth/contacts.other.readonly",
    	"https://www.googleapis.com/auth/contacts.readonly",
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


@login.route("/callback", methods=["GET"])
def callback():
	flow.fetch_token(authorization_response=request.url)
	credentials = flow.credentials
	request_session = requests.session()
	token_google = auth.transport.requests.Request(session=request_session)

	user_google_dict = id_token.verify_oauth2_token(
		id_token=credentials.id_token,
		request=token_google,
		audience=os.getenv("GOOGLE_CLIENT_ID"),
	)
	email = user_google_dict["email"]
	name = user_google_dict["name"]
	user = mongo_client.users.find_one({"email": email})

	if not user:
		new_user = {
			'name': name,
			'email': email,
			'password': set_new_password()
		}
		try:
			user = mongo_client.users.insert_one(new_user)
			return True
		except Exception as exp:
			return {"message": "Algo deu errado ao salvar novo usuário.", "error": exp}

	session["google_id"] = user_google_dict.get("sub")
	session["exp"] = datetime.utcnow() + timedelta(days=1)
	del user_google_dict["aud"]
	del user_google_dict["azp"]
	del user_google_dict["iss"]
	del user_google_dict["sub"]
	del user_google_dict["hd"]
	del user_google_dict["at_hash"]
	del user_google_dict["given_name"]
	del user_google_dict["family_name"]

	token = generate_token_jwt(user_google_dict)
	print(credentials)
	try:
		service = build('people', 'v1', credentials=credentials)
		results = service.people().connections().list(
			resourceName='people/me',
			pageSize=10,
			personFields='names,emailAddresses,photos').execute()
		connections = results.get('connections', [])
		nomes = []
		emails = []
		photos = []
		for person in connections:
			names = person.get('names', [])
			email = person.get('emailAddresses', [])
			photo = person.get("photos", [])
			if names:
				nomes.append(names[0].get('displayName'))
			if email:
				emails.append(email[0].get("value"))
			if photo:
				photos.append(photo[0].get("url"))
		return Response(
		response=json.dumps({"nomes": nomes, "emails": emails, "photos": photos}),
		status=200,
		mimetype="application/json",
	)
	except HttpError as err:
		return Response(
		response=json.dumps({"error": err}),
		status=200,
		mimetype="application/json",
	)
	finally:
		return redirect(f"{os.getenv('FRONTEND_URL')}#/home/?jwt={token}&name={name}")
