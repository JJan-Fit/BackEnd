from collections.abc import Callable

from fastapi.testclient import TestClient


def _create_weight(client: TestClient, headers: dict[str, str], kg: float) -> int:
    response = client.post("/weights", json={"kg": kg}, headers=headers)
    assert response.status_code == 201
    return int(response.json()["data"]["weight_id"])


def test_delete_own_weight_returns_204(client: TestClient, auth_headers: dict[str, str]) -> None:
    weight_id = _create_weight(client, auth_headers, 70.0)

    response = client.delete(f"/weights/{weight_id}", headers=auth_headers)
    assert response.status_code == 204

    listing = client.get("/weights", headers=auth_headers).json()
    assert listing["data"] == []


def test_delete_other_users_weight_returns_404(
    client: TestClient,
    signup_and_token: Callable[..., tuple[int, str]],
) -> None:
    _, alice_token = signup_and_token(email="alice@example.com", nickname="alice")
    _, bob_token = signup_and_token(email="bob@example.com", nickname="bob")
    alice = {"Authorization": f"Bearer {alice_token}"}
    bob = {"Authorization": f"Bearer {bob_token}"}

    alice_weight = _create_weight(client, alice, 60.0)

    response = client.delete(f"/weights/{alice_weight}", headers=bob)
    body = response.json()
    assert response.status_code == 404
    assert body["error"]["code"] == "WEIGHT_NOT_FOUND"

    # alice 의 데이터는 그대로
    listing = client.get("/weights", headers=alice).json()
    assert len(listing["data"]) == 1


def test_delete_nonexistent_weight_returns_404(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.delete("/weights/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "WEIGHT_NOT_FOUND"


def test_delete_without_token_returns_401(client: TestClient) -> None:
    response = client.delete("/weights/1")
    assert response.status_code == 401
