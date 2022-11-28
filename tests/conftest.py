import pytest

from src.app import create_app
from src.app.routes import routes


mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


@pytest.fixture(scope="session")
def app():
    app_on = create_app('testing')
    routes(app_on)
    return app_on


@pytest.fixture
def logged_in_client(client):

    response = client.post("login/auth/google", headers=headers)
    return response.json["url"]
