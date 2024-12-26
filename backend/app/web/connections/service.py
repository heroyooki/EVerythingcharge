from typing import Dict

from propan import Context, apply_types
from sqlalchemy import update

from app.web.connections.models import Connection


@apply_types
async def update_connection(master_id: str, payload: Dict, session=Context()):
    stmt = update(Connection) \
        .where(Connection.master_id == master_id) \
        .values(**payload)
    await session.execute(stmt)
