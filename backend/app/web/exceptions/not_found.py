from __future__ import annotations

from http import HTTPStatus

from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=HTTPStatus.NOT_FOUND,
                         *args,
                         **kwargs)
