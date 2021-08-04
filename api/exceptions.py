from typing import Optional

from fastapi import HTTPException, status


class BadRequestHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg if msg else "Bad request",
        )


class ForbiddenHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=msg if msg else "Requested resource is forbidden",
        )


class NotFoundHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg if msg else "Requested resource is not found",
        )


class ConflictHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg if msg else "Conflicting resource request",
        )


class ServiceNotAvailableHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg if msg else "Service not available",
        )


class UnprocessableEntityHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg if msg else "The entity couldn't be processed",
        )


class AuthFailedHTTPException(HTTPException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg if msg else "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
