from typing import List

from propan import Context
from propan import apply_types
from sqlalchemy import select

from api.web.networks.models import Network
from api.web.networks.views import CreateNetworkPayloadView


@apply_types
async def create_network(data: CreateNetworkPayloadView, session=Context()):
    network = Network(**data.dict())
    session.add(network)
    await session.flush()
    return network


@apply_types
async def get_networks(session=Context()) -> List[Network]:
    query = await session.execute(select(Network))
    return query.scalars().unique().all()
