from typing import Callable

from fastapi import APIRouter as Router
from fastapi import Request, Response
from fastapi.routing import APIRoute

from api.web.exceptions import NotAuthenticated


class AuthRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            response: Response = await original_route_handler(request)
            return response

        return custom_route_handler


class PublicAPIRouter(Router):
    pass


class PrivateAPIRouter(Router):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route_class = AuthRoute
