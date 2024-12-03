import re
from traceback import format_exc

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from propan import apply_types, Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from core.dependencies import get_settings


async def format_custom_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=dict(detail=exc.detail, key=getattr(exc, "key", None)),
    )


async def unique_violation_exception_handler(request: Request, exc: IntegrityError):
    pattern = re.compile(r"Key \((.*?)\)=\((.*?)\) (.*)")
    name, value, reason = pattern.search(exc.args[0]).groups()
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=dict(detail=f"'{value}' {reason}", key=name),
    )


@apply_types
async def unexpected_exceptions_handler(
        request: Request,
        exc: Exception,
        settings=Depends(get_settings)
):
    _exc = format_exc()
    logger.error("Caught unexcpected server error: %r" % format_exc())
    if settings.DEBUG:
        content = _exc
    else:
        content = "Something went wrong."
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
