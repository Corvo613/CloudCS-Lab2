# -*- coding: utf-8 -*-
import pytest
from fastapi.testclient import TestClient


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {"access_token": "token"}


def init_test_client(monkeypatch):
    def mock_make_inference(*args, **kwargs) -> dict[str, float]:
        return {"mpg": 48.239}

    def mock_load_model(*args, **kwargs) -> None:
        return None

    monkeypatch.setenv("MODEL_PATH", "faked/model.pkl")
    monkeypatch.setattr("model_utils.make_inference", mock_make_inference)
    monkeypatch.setattr("model_utils.load_model", mock_load_model)


@pytest.fixture
def init_test_client_with_auth(monkeypatch) -> TestClient:
    def mock_get_request(*args, **kwargs):
        response = FakeResponse(200)
        return response
    
    init_test_client(monkeypatch)
    monkeypatch.setattr("requests.get", mock_get_request)

    from main import app
    return TestClient(app)


@pytest.fixture
def init_test_client_without_auth(monkeypatch) -> TestClient:    
    def mock_get_request(*args, **kwargs):
        response = FakeResponse(401)
        return response

    init_test_client(monkeypatch)
    monkeypatch.setattr("requests.get", mock_get_request)

    from main import app
    return TestClient(app)


def test_healthcheck(init_test_client_with_auth) -> None:
    response = init_test_client_with_auth.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_token_correctness(init_test_client_with_auth) -> None:
    response = init_test_client_with_auth.post(
        "/predictions",
        headers={"Authorization": "Bearer 00000"},
        json={"cylinders": 0, "displacement": 0, "horsepower": 0,
              "weight": 0, "acceleration": 0, "model_year": 0, "origin": 0}
    )
    assert response.status_code == 200
    assert "mpg" in response.json()


def test_token_not_correctness(init_test_client_without_auth):
    response = init_test_client_without_auth.post(
        "/predictions",
        headers={"Authorization": "Bearer kedjkj"},
        json={"cylinders": 0, "displacement": 0, "horsepower": 0,
              "weight": 0, "acceleration": 0, "model_year": 0, "origin": 0}
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid authentication credentials"
    }


def test_token_absent(init_test_client_without_auth):
    response = init_test_client_without_auth.post(
        "/predictions",
        json={"cylinders": 0, "displacement": 0, "horsepower": 0,
              "weight": 0, "acceleration": 0, "model_year": 0, "origin": 0}
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_inference(init_test_client_with_auth):
    response = init_test_client_with_auth.post(
        "/predictions",
        headers={"Authorization": "Bearer 00000"},
        json={"cylinders": 4, "displacement": 113.0, "horsepower": 95.0,
              "weight": 2228.0, "acceleration": 14.0, "model_year": 71,
              "origin": 3}
    )
    assert response.status_code == 200
    assert response.json()["mpg"] == 48.239


def test_current_user(init_test_client_with_auth):
    response = init_test_client_with_auth.get(
        "/users/me",
        headers={"Authorization": "Bearer 0000"}
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "token"}


def test_current_user_without_auth(init_test_client_without_auth):
    response = init_test_client_without_auth.get(
        "/users/me",
        headers={"Authorization": "Bearer 0000"}
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid authentication credentials"
    }
