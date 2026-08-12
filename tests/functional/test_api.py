import threading

import pytest
import requests
from naas.app import app
from werkzeug.serving import make_server


@pytest.fixture(scope="module")
def api_url():
    server = make_server("127.0.0.1", 5050, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield "http://127.0.0.1:5050"

    server.shutdown()
    thread.join(timeout=5)


@pytest.mark.functional
@pytest.mark.parametrize(
    "path",
    [
        "/api/no/fr",
        "/api/no/en",
        "/api/hireme/fr",
        "/api/hireme/en",
        "/api/dateme/fr",
    ],
)
def test_api_returns_a_response(api_url, path):
    response = requests.get(f"{api_url}{path}", timeout=5)
    payload = response.json()

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert isinstance(payload["reason"], str)
    assert payload["reason"].strip()


@pytest.mark.functional
def test_api_rejects_unknown_language(api_url):
    response = requests.get(f"{api_url}/api/no/unknown", timeout=5)

    assert response.status_code == 404
    assert response.json() == {"error": "Language not supported"}
