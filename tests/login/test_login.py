import requests


# TESTS PARA LOGIN

def test_authorization_url_success(client):
    
    response = client.post("login/auth/google", headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    assert response.status_code == 200
    assert "url" in response.json


def test_authorization_url_failed(client):
    
    response = client.get("login/auth/google")
    
    assert response.status_code == 405
    assert response.json == None


def test_authorization_wrong_url_404(client):
    
    response = client.get("login/")
    
    assert response.status_code == 404
    assert response.json == None


def test_url_redirect_OAuth_success(client):

	oauth_url = client.post("login/auth/google", headers={
		"Content-Type": "application/json",
		"Accept": "application/json"
		}).json["url"]

	response = requests.get(oauth_url)

	assert response.status_code == 200
	assert "Fazer login usando sua Conta do Google" or "Sign in - Google Accounts" in response.text
