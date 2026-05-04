import jwt
import pytest

from app.auth import security
from app.core.config import settings


def test_hash_password_is_not_plaintext() -> None:
    hashed = security.hash_password("secret123")
    assert hashed != "secret123"
    assert hashed.startswith("$2")  # bcrypt prefix


def test_verify_password_round_trip() -> None:
    hashed = security.hash_password("secret123")
    assert security.verify_password("secret123", hashed) is True
    assert security.verify_password("wrong", hashed) is False


def test_create_and_decode_access_token() -> None:
    token = security.create_access_token(subject="42")
    payload = security.decode_token(token)
    assert payload["sub"] == "42"
    assert payload["exp"] > payload["iat"]


def test_decode_expired_token_raises() -> None:
    expired = jwt.encode(
        {"sub": "1", "iat": 0, "exp": 1},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        security.decode_token(expired)


def test_decode_token_with_wrong_secret_raises() -> None:
    token = jwt.encode({"sub": "1"}, "other-secret", algorithm=settings.jwt_algorithm)
    with pytest.raises(jwt.InvalidSignatureError):
        security.decode_token(token)
