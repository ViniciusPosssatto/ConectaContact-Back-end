def test_app_name_is(app):
  	assert app.name == "src.app"


def test_app_not_is_name_failed(app):
  	assert app.name != "aplicação qualquer"


def test_config_is_loaded(config):
  	assert config['DEBUG'] is True


def test_request_returns_404(client):
  	assert client.get('/').status_code == 404

