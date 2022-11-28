import requests


def test_app_name_is(app):
  	assert app.name == "src.app"


def test_app_not_is_name_failed(app):
  	assert app.name != "aplicação qualquer"


def test_config_is_loaded(config):
  	assert config['DEBUG'] is True


def test_request_returns_404(client):
  	assert client.get('/').status_code == 404

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

# TESTS PARA CONTACTS

def test_get_contacts_by_user_success(client):

	response = client.get("contacts/637ff045f9394498fb0f76e4")
    
	assert response.status_code == 200
	assert "results" in response.json


def test_get_contacts_by_user_failed(client):

	response = client.get("contacts/1")
    
	assert response.status_code == 400
	assert "erro" in response.json
	assert response.json["erro"] == 'Não foi possível acessar este ID ou usuário não existe'


def test_get_domains_by_user_failed(client):

	response = client.get("contacts/domain/1")
    
	assert response.status_code == 400
	assert "erro" in response.json
	assert response.json["erro"] == 'Não foi possível acessar este ID ou usuário não existe'


def test_get_domains_by_user_success(client):

	response = client.get("contacts/domain/637ff045f9394498fb0f76e4")
    
	assert response.status_code == 200
	assert "domains" in response.json


def test_get_domains_by_path_wrong(client):

	response = client.get("contacts/algumacoisa/637ff045f9394498fb0f76e4")
    
	assert response.status_code == 404
	assert response.json == None
