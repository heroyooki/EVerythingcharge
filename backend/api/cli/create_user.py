import argparse
import asyncio

from loguru import logger
from sqlalchemy.exc import IntegrityError, DBAPIError

from api.web.users.service import create_user
from api.web.users.views import CreateUserView
from core.models import get_contextual_session


async def run(
        email: str,
        password: str,
        first_name: str,
        last_name: str,
):
    view = CreateUserView(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    async with get_contextual_session() as session:
        user = await create_user(
            data=view.dict(exclude_none=True),
            session=session
        )
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

    asyncio.run(
        run(
            email=args.email,
            password=args.password,
            first_name=args.first_name,
            last_name=args.last_name
        )
    )
