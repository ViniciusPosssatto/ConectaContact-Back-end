import os
import json
import requests
from bson import json_util, ObjectId
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
	user = mongo_client.users_login.find_one({"email": email})


	session["google_id"] = user_google_dict.get("sub")
	session["exp"] = datetime.utcnow() + timedelta(days=1)
	del user_google_dict["aud"]
	del user_google_dict["azp"]
	del user_google_dict["iss"]
	del user_google_dict["sub"]
	del user_google_dict["at_hash"]
	del user_google_dict["given_name"]
	del user_google_dict["family_name"]

	token = generate_token_jwt(user_google_dict)

	if not user:
		new_user = {
			'name': name,
			'email': email,
			'password': set_new_password()
		}
		try:
			user = mongo_client.users_login.insert_one(new_user)
		except Exception as exp:
			return {"message": "Algo deu errado ao salvar novo usuário.", "error": exp}
		finally:
			user = mongo_client.users_login.find_one({"email": email})

			
	try:
		service = build('people', 'v1', credentials=credentials)
		results = service.people().connections().list(
			resourceName='people/me',
			pageSize=2000,
			personFields='names,emailAddresses,photos').execute()
		connections = results.get('connections', [])
		contacts = []
		for person in connections:
			names = person.get('names', [])
			email = person.get('emailAddresses', [])
			photo = person.get("photos", [])
			if email:
				if not person.get("names"):
					name = email[0].get("value")
					contacts.append({"name": name, "email": email[0].get("value"), "photo": photo[0].get("url"), "id_user": user.get("_id")})
				else:
					contacts.append({"name": names[0].get('displayName'), "email": email[0].get("value"), "photo": photo[0].get("url"), "id_user": user.get("_id")})
		
		for contact in contacts:
			contact_exists =  mongo_client.contacts.find_one({"email": contact.get("email"), "id_user": ObjectId(user.get('_id'))})
			if not contact_exists: 
				mongo_client.contacts.insert_one(contact)


		# res = service.people().otherContacts().list(
		# 	pageSize=10, 
		# 	readMask="names,emailAddresses,photos"
		# ).execute()


		return Response(
		response=json_util.dumps(contacts),
		status=200,
		mimetype="application/json",
	)
	except HttpError as err:
		print("error HTTPerror ="  , err)
	except Exception as err:
		print("error Exception ="  , err)
		return Response(
		response={"error": err},
		status=400,
		mimetype="application/json",
	)
	# # finally:
	# 	return redirect(f"{os.getenv('FRONTEND_URL')}#/home/?jwt={token}&name={name}")
