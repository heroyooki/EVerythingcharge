import argparse
import asyncio
from typing import Any

from loguru import logger
from propan import apply_types, Depends
from propan.annotations import ContextRepo
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from api.web.users import get_users_service
from api.web.users.views import CreateUserView
from core.models import get_session


@apply_types
async def run(
        email,
        password,
        first_name,
        last_name,
        context: ContextRepo,
        service: Any = Depends(get_users_service),
        session: AsyncSession = Depends(get_session),
):
    with context.scope("session", session):
        view = CreateUserView(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user = await service.create_user(data=view.dict(exclude_none=True))
        try:
            await session.commit()
        except IntegrityError:
            logger.warning("The user with given email already exists.")
            return
        except DBAPIError:
            logger.error("Too long value.")
            return

    logger.success(f"Successfully created user with email={user.email} and password={password}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--email", type=str, required=True)
    parser.add_argument("-p", "--password", type=str, required=True)
    parser.add_argument("-f", "--first_name", type=str, required=True)
    parser.add_argument("-l", "--last_name", type=str, required=True)
    args = parser.parse_args()

    asyncio.run(run(
        email=args.email,
        password=args.password,
        first_name=args.first_name,
        last_name=args.last_name
    ))
