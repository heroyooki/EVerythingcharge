from typing import Dict, List

from propan import Context
from propan import apply_types
from sqlalchemy import delete

from app.web.grids.models import Grid


@apply_types
async def create_grid(data: Dict, session=Context()):
    grid = Grid(**data)
    session.add(grid)
    await session.flush()
    return grid


@apply_types
async def delete_grids(grid_ids: List[str], session=Context()):
    query = delete(Grid).where(Grid.id.in_(grid_ids))
    await session.execute(query)
