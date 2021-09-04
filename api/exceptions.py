from typing import Optional

from fastapi import HTTPException, status


def _open_api(default: str, msg: Optional[str] = None):
    return {
        "content": {
            "application/json": {
                "example": {
                    "detail": msg if msg else default,
                },
            },
        },
    }


class BadRequestHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg if msg else "Bad request",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Bad request", msg)


class ForbiddenHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=msg if msg else "Requested resource is forbidden",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Requested resource is forbidden", msg)


class NotFoundHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg if msg else "Requested resource is not found",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Requested resource is not found", msg)


class ConflictHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg if msg else "Conflicting resource request",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Conflicting resource request", msg)


class ServiceNotAvailableHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg if msg else "Service not available",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Service not available", msg)


class UnprocessableEntityHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg if msg else "The entity couldn't be processed",
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("The entity couldn't be processed", msg)


class AuthFailedHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg if msg else "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def open_api(msg: Optional[str] = None):
        return _open_api("Could not validate credentials", msg)
