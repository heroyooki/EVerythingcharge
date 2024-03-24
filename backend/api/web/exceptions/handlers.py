import re
from traceback import format_exc

from fastapi import Request
from loguru import logger
from propan import apply_types, Depends
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import JSONResponse

from core.utils import get_settings


async def unique_violation_exception_handler(request: Request, exc: IntegrityError):
    pattern = re.compile(r"Key \((.*?)\)=\((.*?)\) (.*)")
    name, value, reason = pattern.search(exc.args[0]).groups()
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=dict(detail=f"'{value}' {reason}", key=name),
    )


@apply_types
async def common_exceptions_handler(
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
