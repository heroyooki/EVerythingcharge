from __future__ import annotations

from http import HTTPStatus

from fastapi import HTTPException


class NotAuthenticated(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            *args,
            **kwargs
        )
