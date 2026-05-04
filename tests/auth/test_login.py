from fastapi.testclient import TestClient

from app.auth import security


def _signup(client: TestClient, email: str, password: str = "secret123") -> None:
    response = client.post(
        "/auth/signup",
        json={"email": email, "password": password, "nickname": email.split("@")[0]},
    )
    assert response.status_code == 201


def test_login_success_returns_token(client: TestClient) -> None:
    _signup(client, "lo@example.com")
    response = client.post(
        "/auth/login",
        json={"email": "lo@example.com", "password": "secret123"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["token_type"] == "bearer"
    assert body["data"]["access_token"]
    assert body["data"]["expires_in"] > 0

    payload = security.decode_token(body["data"]["access_token"])
    assert payload["sub"].isdigit()


def test_login_wrong_password_returns_401(client: TestClient) -> None:
    _signup(client, "wp@example.com")
    response = client.post(
        "/auth/login",
        json={"email": "wp@example.com", "password": "wrong-password"},
    )
    body = response.json()
    assert response.status_code == 401
    assert body["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


def test_login_unknown_email_returns_401(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        json={"email": "ghost@example.com", "password": "secret123"},
    )
    body = response.json()
    assert response.status_code == 401
    assert body["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


def test_login_email_is_case_insensitive(client: TestClient) -> None:
    _signup(client, "case@example.com")
    response = client.post(
        "/auth/login",
        json={"email": "CASE@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
