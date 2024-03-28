import http

from fastapi import Response, Depends, Request

from api.web.exceptions import NotAuthenticated
from api.web.routing import PublicAPIRouter, PrivateAPIRouter
from api.web.users.models import User
from api.web.users.service import AnnotatedUser, Password, PasswdContext, create_user
from api.web.users.views import UserView

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
async def receive_current_user(request: Request):
    return request.user


@public_router.post("/login")
async def login(
        response: Response,
        password: Password,
        user: AnnotatedUser,
        passwd_context: PasswdContext,
):
    if not user or not passwd_context.verify(password, user.password):
        raise NotAuthenticated(detail="Invalid login or password")
    response.headers["X-Authenticated"] = user.id
    response.status_code = http.HTTPStatus.ACCEPTED
    return response


@private_router.delete("/logout")
async def logout():
    raise NotAuthenticated()
