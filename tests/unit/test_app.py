from unittest.mock import patch

import pytest
from naas.app import app, cache, load_items


@pytest.fixture()
def client():
    app.config.update(TESTING=True)

    cache.clear()

    with app.test_client() as test_client:
        yield test_client

    cache.clear()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("category", "language"),
    [
        ("reason", "fr"),
        ("reason", "en"),
        ("reason", "es"),
        ("hireme", "fr"),
        ("hireme", "en"),
        ("hireme", "es"),
        ("dateme", "fr"),
    ],
)
def test_load_items(category, language):
    items = load_items(category, language)

    assert isinstance(items, list)
    assert items
    assert all(isinstance(item, str) for item in items)


@pytest.mark.unit
def test_load_items_uses_cache():
    first_result = load_items("reason", "fr")

    with patch("pathlib.Path.open") as mocked_open:
        second_result = load_items("reason", "fr")

    assert second_result is first_result
    mocked_open.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/api/no",
        "/api/hireme",
        "/api/dateme",
    ],
)
def test_html_pages(client, path):
    response = client.get(path)

    assert response.status_code == 200
    assert response.content_type.startswith("text/html")


@pytest.mark.unit
@pytest.mark.parametrize(
    "path",
    [
        "/api/no/fr",
        "/api/no/en",
        "/api/no/es",
        "/api/hireme/fr",
        "/api/hireme/en",
        "/api/hireme/es",
        "/api/dateme/fr",
    ],
)
def test_supported_endpoint(client, path):
    response = client.get(path)
    payload = response.get_json()

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert isinstance(payload["reason"], str)
    assert payload["reason"].strip()


@pytest.mark.unit
@pytest.mark.parametrize(
    "path",
    [
        "/api/no/unknown",
        "/api/hireme/unknown",
        "/api/dateme/unknown",
    ],
)
def test_unsupported_language(client, path):
    response = client.get(path)

    assert response.status_code == 404
    assert response.get_json() == {"error": "Language not supported"}
