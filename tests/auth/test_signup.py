from fastapi.testclient import TestClient


def test_signup_creates_member_and_returns_envelope(client: TestClient) -> None:
    response = client.post(
        "/auth/signup",
        json={"email": "user@example.com", "password": "secret123", "nickname": "user"},
    )
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["email"] == "user@example.com"
    assert body["data"]["nickname"] == "user"
    assert isinstance(body["data"]["member_id"], int)
    assert "created_at" in body["data"]


def test_signup_duplicate_email_returns_409(client: TestClient) -> None:
    payload = {"email": "dup@example.com", "password": "secret123", "nickname": "dup"}
    first = client.post("/auth/signup", json=payload)
    assert first.status_code == 201

    second = client.post("/auth/signup", json=payload)
    body = second.json()
    assert second.status_code == 409
    assert body["success"] is False
    assert body["error"]["code"] == "EMAIL_ALREADY_TAKEN"


def test_signup_short_password_returns_422(client: TestClient) -> None:
    response = client.post(
        "/auth/signup",
        json={"email": "x@example.com", "password": "short", "nickname": "x"},
    )
    body = response.json()
    assert response.status_code == 422
    assert body["error"]["code"] == "VALIDATION_FAILED"


def test_signup_invalid_email_returns_422(client: TestClient) -> None:
    response = client.post(
        "/auth/signup",
        json={"email": "not-an-email", "password": "secret123", "nickname": "x"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_FAILED"


def test_signup_does_not_leak_password_hash(client: TestClient) -> None:
    response = client.post(
        "/auth/signup",
        json={"email": "n@example.com", "password": "secret123", "nickname": "n"},
    )
    body = response.json()
    assert "password" not in body["data"]
