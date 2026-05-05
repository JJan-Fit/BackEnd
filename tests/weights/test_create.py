from fastapi.testclient import TestClient


def test_create_weight_returns_envelope(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post("/weights", json={"kg": 70.5}, headers=auth_headers)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["error"] is None
    assert isinstance(body["data"]["weight_id"], int)
    assert float(body["data"]["kg"]) == 70.5
    assert "created_at" in body["data"]


def test_create_weight_without_token_returns_401(client: TestClient) -> None:
    response = client.post("/weights", json={"kg": 70.5})
    body = response.json()
    assert response.status_code == 401
    assert body["error"]["code"] == "UNAUTHORIZED"


def test_create_weight_with_negative_kg_returns_422(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post("/weights", json={"kg": -1.0}, headers=auth_headers)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_FAILED"


def test_create_weight_with_zero_kg_returns_422(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post("/weights", json={"kg": 0}, headers=auth_headers)
    assert response.status_code == 422


def test_create_weight_exceeding_max_returns_422(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post("/weights", json={"kg": 1000.00}, headers=auth_headers)
    assert response.status_code == 422
