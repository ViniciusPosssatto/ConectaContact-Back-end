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
