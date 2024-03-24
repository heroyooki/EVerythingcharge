from typing import List

from fastapi import Depends
from starlette import status

from api.web.networks.models import Network
from api.web.networks.service import create_network, get_networks
from api.web.networks.views import NetworkView
from api.web.routing import PrivateAPIRouter

private_router = PrivateAPIRouter(prefix="/networks")


@private_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=NetworkView
)
async def add_network(network: Network = Depends(create_network)):
    return network


@private_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[NetworkView]
)
async def list_networks(networks: List[Network] = Depends(get_networks)):
    return networks
