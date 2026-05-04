"""API 응답 envelope.

모든 도메인 라우터는 ``ApiResponse[T]`` 를 응답 모델로 사용해 일관된 형태를
반환한다. 성공/실패 어느 쪽이든 다음 키를 가진다:

    {"success": bool, "data": T | None, "error": ApiError | None}

성공 응답 helper: :func:`ok`. 실패는 보통 ``app/shared/exceptions.py`` 의
``AppException`` 을 raise → 핸들러가 자동 envelope.
"""

from typing import Any

from pydantic import BaseModel


class ApiError(BaseModel):
    code: str
    message: str
    detail: dict[str, Any] | None = None


class ApiResponse[T](BaseModel):
    success: bool
    data: T | None = None
    error: ApiError | None = None


def ok[T](data: T | None = None) -> ApiResponse[T]:
    return ApiResponse[T](success=True, data=data)


def fail(
    code: str,
    message: str,
    detail: dict[str, Any] | None = None,
) -> ApiResponse[None]:
    return ApiResponse[None](
        success=False,
        error=ApiError(code=code, message=message, detail=detail),
    )
