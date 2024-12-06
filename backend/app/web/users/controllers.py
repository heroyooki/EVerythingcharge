import http
from typing import List

from fastapi import Response, Depends, Request

from app.web.exceptions import NotAuthenticated
from app.web.networks.models import Network
from app.web.networks.service import get_networks
from app.web.routing import PublicAPIRouter, PrivateAPIRouter
from app.web.users.models import User
from app.web.users.service import AnnotatedUser, Password, PasswdContext, create_user
from app.web.users.views import UserView

public_router = PublicAPIRouter()
private_router = PrivateAPIRouter()


@private_router.post(
    "/users",
    status_code=http.HTTPStatus.CREATED,
    response_model=UserView
)
async def add_user(user: User = Depends(create_user)):
    return user


@private_router.get(
    "/me",
    status_code=http.HTTPStatus.OK,
    response_model=UserView
)
async def receive_current_user(
        request: Request,
        networks: List[Network] = Depends(get_networks)
):
    view = UserView.from_orm(request.user)
    view.networks = networks
    return view


@public_router.post("/login")
async def login(
        response: Response,
        password: Password,
        user: AnnotatedUser,
        passwd_context: PasswdContext,
):
    if not user:
        raise NotAuthenticated(detail="Unrecognized email.", key="email")
    if not passwd_context.verify(password, user.password):
        raise NotAuthenticated(detail="Invalid password.", key="password")
    response.headers["X-Authenticated"] = user.id
    response.status_code = http.HTTPStatus.ACCEPTED
    return response


@private_router.delete("/logout")
async def logout():
    raise NotAuthenticated()
