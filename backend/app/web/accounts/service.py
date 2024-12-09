from typing import Dict, List

from propan import Context
from propan import apply_types
from sqlalchemy import delete

from app.web.accounts.models import Account


@apply_types
async def create_account(data: Dict, session=Context()):
    account = Account(**data)
    session.add(account)
    await session.flush()
    return account


@apply_types
async def delete_accounts(grid_ids: List[str], session=Context()):
    query = delete(Account).where(Account.id.in_(grid_ids))
    await session.execute(query)
