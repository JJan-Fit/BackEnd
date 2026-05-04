"""FastAPI 예외 핸들러 — 모든 에러를 :class:`ApiResponse` envelope 으로 통일."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.exceptions import AppException
from app.shared.response import ApiError, ApiResponse

logger = logging.getLogger(__name__)


def _envelope(status_code: int, error: ApiError) -> JSONResponse:
    body = ApiResponse[Any](success=False, error=error).model_dump(mode="json")
    return JSONResponse(status_code=status_code, content=body)


async def app_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppException)
    return _envelope(
        exc.status_code,
        ApiError(code=exc.code, message=exc.message, detail=exc.detail),
    )


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    return _envelope(
        exc.status_code,
        ApiError(code=f"HTTP_{exc.status_code}", message=str(exc.detail)),
    )


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    return _envelope(
        422,
        ApiError(
            code="VALIDATION_FAILED",
            message="입력값 검증에 실패했습니다.",
            detail={"errors": exc.errors()},
        ),
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception", exc_info=exc)
    return _envelope(
        500,
        ApiError(code="INTERNAL_ERROR", message="내부 오류가 발생했습니다."),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
