import math
from typing import Tuple, List

from fastapi import Query
from propan import Context, apply_types
from sqlalchemy import func, select

from api.web.views import PaginationView


def params_extractor(
        page: int = Query(1, ge=1),
        size: int = Query(10, gt=0),
        search: str = Query("")
) -> Tuple:
    return page, size, search


@apply_types
async def paginate(
        query_builder,
        params,
        session=Context(),
        **kwargs
) -> Tuple[List, PaginationView]:
    page, size, search = params
    query = await query_builder(search=search, **kwargs)
    count = await session.execute(select(func.count()) \
                                  .select_from(query.alias('subquery')))
    query = query.limit(size).offset(size * (page - 1))

    result = await session.execute(query)
    items = result.unique().scalars().fetchall()

    total = count.scalar()
    pagination = PaginationView(
        current_page=page,
        last_page=math.ceil(total / size) or 1,
        total=total
    )

    return items, pagination
