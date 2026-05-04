from collections.abc import Callable

from fastapi.testclient import TestClient


def test_list_returns_only_own_weights_in_desc_order(
    client: TestClient,
    signup_and_token: Callable[..., tuple[int, str]],
) -> None:
    _, alice_token = signup_and_token(email="alice@example.com", nickname="alice")
    _, bob_token = signup_and_token(email="bob@example.com", nickname="bob")
    alice = {"Authorization": f"Bearer {alice_token}"}
    bob = {"Authorization": f"Bearer {bob_token}"}

    client.post("/weights", json={"kg": 60.0}, headers=alice)
    client.post("/weights", json={"kg": 60.5}, headers=alice)
    client.post("/weights", json={"kg": 99.9}, headers=bob)

    response = client.get("/weights", headers=alice)
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["data"]) == 2
    kgs = [float(item["kg"]) for item in body["data"]]
    # 최신 → 과거 순
    assert kgs == [60.5, 60.0]


def test_list_empty_for_new_user(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.get("/weights", headers=auth_headers)
    body = response.json()
    assert response.status_code == 200
    assert body["data"] == []


def test_list_without_token_returns_401(client: TestClient) -> None:
    response = client.get("/weights")
    assert response.status_code == 401
