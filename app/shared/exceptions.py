"""도메인/HTTP 의미론적 예외.

라우터/서비스 내부에서는 ``raise NotFound(...)`` 처럼 도메인 레벨 예외를
던지고, 핸들러(:mod:`app.shared.handlers`)가 적절한 HTTP 상태와 응답
envelope 으로 변환한다. 라우터에서 ``HTTPException`` 직접 raise 는 지양.
"""

from typing import Any


class AppException(Exception):
    """모든 도메인 예외의 기반 클래스."""

    code: str = "INTERNAL_ERROR"
    message: str = "내부 오류가 발생했습니다."
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        *,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message or self.message)
        if message is not None:
            self.message = message
        self.detail = detail


class BadRequest(AppException):
    code = "BAD_REQUEST"
    message = "잘못된 요청입니다."
    status_code = 400


class Unauthorized(AppException):
    code = "UNAUTHORIZED"
    message = "인증이 필요합니다."
    status_code = 401


class Forbidden(AppException):
    code = "FORBIDDEN"
    message = "권한이 없습니다."
    status_code = 403


class NotFound(AppException):
    code = "NOT_FOUND"
    message = "리소스를 찾을 수 없습니다."
    status_code = 404


class Conflict(AppException):
    code = "CONFLICT"
    message = "리소스가 이미 존재합니다."
    status_code = 409


class ValidationFailed(AppException):
    code = "VALIDATION_FAILED"
    message = "입력값 검증에 실패했습니다."
    status_code = 422
