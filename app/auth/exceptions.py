from app.shared.exceptions import AppException


class EmailAlreadyTaken(AppException):
    code = "EMAIL_ALREADY_TAKEN"
    message = "이미 가입된 이메일입니다."
    status_code = 409


class InvalidCredentials(AppException):
    code = "AUTH_INVALID_CREDENTIALS"
    message = "이메일 또는 비밀번호가 올바르지 않습니다."
    status_code = 401


class TokenInvalid(AppException):
    code = "AUTH_TOKEN_INVALID"
    message = "토큰이 유효하지 않습니다."
    status_code = 401


class TokenExpired(AppException):
    code = "AUTH_TOKEN_EXPIRED"
    message = "토큰이 만료되었습니다."
    status_code = 401
