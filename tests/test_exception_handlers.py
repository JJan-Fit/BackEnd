from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.shared.exceptions import Conflict, NotFound, Unauthorized
from app.shared.handlers import register_exception_handlers


def _make_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    class Body(BaseModel):
        amount: int

    @app.post("/echo")
    def echo(body: Body) -> dict[str, int]:
        return {"amount": body.amount}

    @app.get("/raise/not-found")
    def raise_not_found() -> None:
        raise NotFound()

    @app.get("/raise/unauthorized-custom")
    def raise_unauthorized() -> None:
        raise Unauthorized("토큰이 만료되었습니다.")

    @app.get("/raise/conflict")
    def raise_conflict() -> None:
        raise Conflict(detail={"email": "이미 가입된 이메일입니다."})

    @app.get("/raise/http-exc")
    def raise_http_exc() -> None:
        raise HTTPException(status_code=418, detail="I'm a teapot")

    @app.get("/raise/internal")
    def raise_internal() -> None:
        raise RuntimeError("뭔가 잘못됨")

    return app


client = TestClient(_make_app(), raise_server_exceptions=False)


def test_app_exception_default_envelope() -> None:
    response = client.get("/raise/not-found")
    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "data": None,
        "error": {
            "code": "NOT_FOUND",
            "message": "리소스를 찾을 수 없습니다.",
            "detail": None,
        },
    }


def test_app_exception_message_override() -> None:
    response = client.get("/raise/unauthorized-custom")
    body = response.json()
    assert response.status_code == 401
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert body["error"]["message"] == "토큰이 만료되었습니다."


def test_app_exception_detail_carried_through() -> None:
    response = client.get("/raise/conflict")
    body = response.json()
    assert response.status_code == 409
    assert body["error"]["detail"] == {"email": "이미 가입된 이메일입니다."}


def test_http_exception_wrapped_in_envelope() -> None:
    response = client.get("/raise/http-exc")
    body = response.json()
    assert response.status_code == 418
    assert body["success"] is False
    assert body["error"]["code"] == "HTTP_418"
    assert body["error"]["message"] == "I'm a teapot"


def test_validation_error_returns_envelope() -> None:
    response = client.post("/echo", json={"amount": "not-a-number"})
    body = response.json()
    assert response.status_code == 422
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_FAILED"
    assert "errors" in (body["error"]["detail"] or {})


def test_unhandled_exception_returns_500_envelope() -> None:
    response = client.get("/raise/internal")
    body = response.json()
    assert response.status_code == 500
    assert body["success"] is False
    assert body["error"]["code"] == "INTERNAL_ERROR"
